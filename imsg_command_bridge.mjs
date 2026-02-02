#!/usr/bin/env node
/**
 * iMessage command bridge (SAFE MODE, polling)
 *
 * Watches a specific chat for incoming texts from a single handle and replies.
 * Uses polling (imsg history) instead of imsg watch, because fs-event streaming
 * can be flaky depending on permissions/sandboxing.
 *
 * Protocol (from the allowed number only):
 *   cmd: <shell command>   -> propose command, requires confirm
 *   yes                    -> run last proposed command
 *   no                     -> cancel
 *   help                   -> show instructions
 */

import { spawn } from 'node:child_process';

const WORKDIR = '/Users/anansi/.openclaw/workspace';
const CHAT_ID = Number(process.env.IMSG_CHAT_ID || '1');
const ALLOWED_SENDER = (process.env.IMSG_ALLOWED_SENDER || '+13162592508').trim();

const MAX_OUTPUT_CHARS = 2500;
const CMD_TIMEOUT_MS = 12_000;
const POLL_MS = 900;

let pending = null; // { cmd, ts }
let lastSeenId = null;
let sending = false;

function nowIso() {
  return new Date().toISOString();
}

function isBlocked(cmd) {
  const s = cmd.trim().toLowerCase();
  if (!s) return true;

  // No privilege escalation
  if (/(^|\s)sudo(\s|$)/.test(s)) return true;

  // Block some foot-guns / persistence / process control
  const blocked = [
    ' rm ', 'rm -', 'rm\t', 'rm\n',
    ' shutdown', 'reboot', 'halt',
    ' kill ', 'killall',
    ' launchctl',
    ' systemsetup',
    ' defaults write',
    ' chmod ', ' chown ',
    ' diskutil',
    ' csrutil',
    ' nvram',
    ' scutil',
  ];
  const padded = ` ${s} `;
  if (blocked.some((b) => padded.includes(b))) return true;

  // Block shell redirections that can overwrite files broadly
  if (/[>]{1,2}\s*\S/.test(s)) return true;

  return false;
}

function trunc(s) {
  if (s.length <= MAX_OUTPUT_CHARS) return s;
  return s.slice(0, MAX_OUTPUT_CHARS) + `\n…(truncated to ${MAX_OUTPUT_CHARS} chars)`;
}

function sendText(text) {
  if (sending) return; // basic backpressure
  sending = true;

  const p = spawn('imsg', ['send', '--to', ALLOWED_SENDER, '--service', 'imessage', '--text', text], {
    stdio: 'ignore',
  });

  p.on('close', () => {
    sending = false;
  });

  p.on('error', (e) => {
    // eslint-disable-next-line no-console
    console.error('send error', e);
    sending = false;
  });
}

function runCommand(cmd) {
  return new Promise((resolve) => {
    const child = spawn('/bin/zsh', ['-lc', cmd], {
      cwd: WORKDIR,
      env: { ...process.env },
    });

    let out = '';
    let err = '';

    const t = setTimeout(() => {
      child.kill('SIGKILL');
      resolve({ code: -1, out, err: err + `\nTimed out after ${CMD_TIMEOUT_MS}ms` });
    }, CMD_TIMEOUT_MS);

    child.stdout.on('data', (d) => (out += d.toString('utf8')));
    child.stderr.on('data', (d) => (err += d.toString('utf8')));

    child.on('close', (code) => {
      clearTimeout(t);
      resolve({ code, out, err });
    });
  });
}

function helpText() {
  return [
    `Madness iMessage bridge (${nowIso()})`,
    '',
    'Commands:',
    '  cmd: <command>   propose a command to run on the Mac (confirmation required)',
    '  yes / no         confirm or cancel the pending command',
    '  help             show this message',
    '',
    'Notes:',
    '- No sudo.',
    '- Blocks destructive commands & redirections.',
    `- Runs in: ${WORKDIR}`,
  ].join('\n');
}

async function handleIncoming(msg) {
  const text = (msg.text || '').trim();
  if (!text) return;

  const lower = text.toLowerCase();

  if (lower === 'help') {
    sendText(helpText());
    return;
  }

  if (lower === 'no') {
    pending = null;
    sendText('Cancelled.');
    return;
  }

  if (lower === 'yes') {
    if (!pending) {
      sendText('No pending command. Send `cmd: ...` first.');
      return;
    }

    const cmd = pending.cmd;
    pending = null;

    sendText(`Running:\n${cmd}`);

    const res = await runCommand(cmd);
    const combined = [
      `exit=${res.code}`,
      res.out ? `\nstdout:\n${res.out}` : '',
      res.err ? `\nstderr:\n${res.err}` : '',
    ].join('');

    sendText(trunc(combined.trim() || '(no output)'));
    return;
  }

  const m = text.match(/^cmd:\s*(.+)$/i);
  if (m) {
    const cmd = m[1].trim();
    if (isBlocked(cmd)) {
      sendText('Blocked for safety. Try `cmd: openclaw status` or `cmd: ls` or `cmd: pwd`.');
      return;
    }
    pending = { cmd, ts: Date.now() };
    sendText(`Proposed command:\n${cmd}\n\nReply YES to run, or NO to cancel.`);
    return;
  }

  sendText('Got it. Send `cmd: <command>` if you want me to run something, or `help`.');
}

function execJsonLines(args) {
  return new Promise((resolve, reject) => {
    const p = spawn('imsg', args, { stdio: ['ignore', 'pipe', 'pipe'] });
    let out = '';
    let err = '';
    p.stdout.on('data', (d) => (out += d.toString('utf8')));
    p.stderr.on('data', (d) => (err += d.toString('utf8')));
    p.on('close', (code) => {
      if (code !== 0) return reject(new Error(err || `imsg exited ${code}`));
      const lines = out
        .split('\n')
        .map((l) => l.trim())
        .filter(Boolean)
        .map((l) => JSON.parse(l));
      resolve(lines);
    });
  });
}

async function pollOnce() {
  const rows = await execJsonLines(['history', '--chat-id', String(CHAT_ID), '--limit', '1', '--json']);
  const msg = rows[0];
  if (!msg) return;

  if (lastSeenId == null) {
    lastSeenId = msg.id;
    return;
  }

  if (msg.id === lastSeenId) return;
  if (msg.id < lastSeenId) {
    lastSeenId = msg.id;
    return;
  }

  lastSeenId = msg.id;

  if (msg.is_from_me) return;
  if ((msg.sender || '').trim() !== ALLOWED_SENDER) return;

  await handleIncoming(msg);
}

async function main() {
  // eslint-disable-next-line no-console
  console.log(`Starting iMessage bridge (polling) in ${WORKDIR}`);
  // eslint-disable-next-line no-console
  console.log(`Chat ${CHAT_ID}, allowed sender ${ALLOWED_SENDER}, poll ${POLL_MS}ms`);

  while (true) {
    try {
      await pollOnce();
    } catch (e) {
      // eslint-disable-next-line no-console
      console.error('poll error', e?.message || e);
    }
    await new Promise((r) => setTimeout(r, POLL_MS));
  }
}

main();
