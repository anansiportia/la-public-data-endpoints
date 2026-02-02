# MadnessBot Forum Outreach Drafting Kit

Purpose: reusable, non-spammy replies for automotive forums that are helpful **first**, ask a few clarifying questions, provide **safe** diagnostic steps, and include a light CTA to try MadnessBot.

> **Notes for posting**
> - Keep tone calm and practical; don’t over-promise.
> - Avoid unsafe instructions (bypassing safety systems, fuel/ignition “spark test” without guidance, etc.).
> - When relevant, remind to work on a cool engine, use jack stands, wear eye protection, keep hands/clothes clear of moving parts.
> - Replace bracketed placeholders before posting.

---

## Tracked link + CTA blocks (copy/paste)

### CTA Block A (short)
If you want, you can paste your details into **MadnessBot** (free) and it’ll organize likely causes + next checks:

**Copy/paste prompt:**
```
Vehicle: [year make model engine]
Codes: [list]
Symptoms: [when it happens, noise, smell]
Recent work: [repairs/parts]
Data: [fuel trims, misfire counts, temps, volts]
Goal: [diagnose / confirm fix]
```
Tracked link: **[MADNESSBOT_TRACKED_LINK]**

### CTA Block B (with OBD data)
If you have a scanner, MadnessBot (free) is good at interpreting the numbers:

**Copy/paste prompt:**
```
Vehicle: [year make model engine]
Codes: [list]
Freeze frame: [RPM, load, ECT, STFT/LTFT, speed]
Live data: [O2/AFR, trims, MAP/MAF, misfire counters]
What I’ve tried: [steps]
```
Tracked link: **[MADNESSBOT_TRACKED_LINK]**

### CTA Block C (electrical)
If you’d like a step-by-step electrical test plan tailored to your car, try MadnessBot free:

**Copy/paste prompt:**
```
Vehicle: [year make model]
Issue: [no-crank / parasitic draw / charging]
Battery age: [years]
Voltage readings: [resting / key on / cranking]
Any clicks? lights dim? security light?
Recent changes: [radio/alarms/repairs]
```
Tracked link: **[MADNESSBOT_TRACKED_LINK]**

---

# 10 Reusable Reply Templates

## Template 1 — “Need details + safe baseline checks”
**Helpful opener:**
- That symptom can come from a few different systems, so a couple details will narrow it down fast.

**Clarifying questions (pick 2–3):**
1) What’s the **year/make/model/engine** and mileage?
2) Any **codes** stored (even pending) and can you share **freeze-frame**?
3) Does it happen **cold/hot**, idle/cruise/WOT, and did anything change right before it started?

**Safe diagnostic steps:**
- Start with basics: check battery voltage, obvious vacuum hoses, loose intake clamps, and fluid levels.
- Scan for codes + look at live data that matches the symptom (fuel trims, misfire counters, temps, etc.).
- If you recently replaced parts, re-check connectors, grounds, and that nothing got pinched.

**CTA:**
(Use CTA Block A or B)

---

## Template 2 — “OBD code triage (one code, many causes)”
**Clarifying questions:**
1) Is the code **current or history**? Any other codes alongside it?
2) Can you post **freeze-frame** + key live data (STFT/LTFT, O2/AFR, coolant temp)?
3) Any recent work (spark plugs, O2 sensors, exhaust, intake)?

**Safe diagnostic steps:**
- Confirm it’s reproducible: clear codes, drive until monitors run, re-scan.
- Check common failure points for that code (wiring/connectors/exhaust leaks/vacuum leaks).
- Use data (trims, sensor response) to avoid “parts darts.”

**CTA:**
(Use CTA Block B)

---

## Template 3 — “Misfire template (P0300/P030x)”
**Clarifying questions:**
1) Which engine and do you have **P0300** or specific cylinders (**P0301–P0308**)?
2) When does it misfire (idle, under load, cold start), and is the **CEL flashing**?
3) Have plugs/coils/injectors been replaced—and with what brand?

**Safe diagnostic steps:**
- If CEL is flashing, avoid hard driving (can overheat the catalytic converter).
- Check basics: correct plug gap/torque, coil boots seated, no oil/coolant in plug wells.
- Look at misfire counters per cylinder.
- If you have a specific cylinder code: swap **coil** or **plug** with another cylinder and see if the misfire follows.
- If P0300/random: check for vacuum leaks, low fuel pressure (if you can test safely), and MAF issues.

**CTA:**
(Use CTA Block B)

---

## Template 4 — “Catalyst efficiency (P0420/P0430)”
**Clarifying questions:**
1) Any misfire/fuel trim codes *before* the catalyst code?
2) Any exhaust work, leaks, or aftermarket parts?
3) What’s the mileage and is oil consumption/coolant loss present?

**Safe diagnostic steps:**
- Fix upstream issues first (misfires, rich/lean, exhaust leaks).
- Check for exhaust leaks near the manifold/front pipe (listen for ticking when cold).
- Compare upstream vs downstream O2 sensor behavior (downstream should be steadier).
- Avoid replacing the cat until data supports it.

**CTA:**
(Use CTA Block B)

---

## Template 5 — “No-crank / clicks / starts sometimes”
**Clarifying questions:**
1) When you turn the key, do you get **no sound**, **single click**, or **rapid clicks**?
2) What’s battery voltage at rest and **during crank** (if it cranks at all)?
3) Any security/immobilizer light behavior? Any recent battery/alternator work?

**Safe diagnostic steps:**
- Check battery terminals for tight/clean connections (including ground to body/engine).
- Try a jump start from a known-good source; observe whether behavior changes.
- If it clicks: measure voltage drop across battery cables (or feel for hot cables after a start attempt).
- Verify the starter relay/fuse and that the vehicle is in Park/Neutral (neutral safety switch symptoms).

**CTA:**
(Use CTA Block C)

---

## Template 6 — “Overheating / coolant loss”
**Clarifying questions:**
1) Does it overheat at idle, highway, or both?
2) Are you losing coolant, and do you see leaks (wet spots, smell)?
3) Any recent work (thermostat, water pump), and does the heater blow hot?

**Safe diagnostic steps:**
- Don’t open a hot cooling system; let it cool fully.
- Confirm coolant level when cold, and inspect for external leaks (radiator seams, hoses, water pump weep hole).
- Check radiator fan operation (A/C on often commands fans).
- If heater goes cold when overheating, suspect air in system or low coolant.
- Pressure test is best if available; otherwise watch for bubbling in reservoir after warm-up (not definitive).

**CTA:**
(Use CTA Block A)

---

## Template 7 — “Parasitic draw / battery dead overnight”
**Clarifying questions:**
1) How old is the battery and has it tested good (CCA)?
2) How long until it’s dead (hours vs days), and any aftermarket electronics?
3) Do you have a multimeter and are you comfortable measuring current safely?

**Safe diagnostic steps:**
- Confirm charging system works first (13.8–14.7V typical while running; varies).
- Perform a parasitic draw test: let modules go to sleep, measure current in series (or use a clamp meter).
- Pull fuses one at a time to isolate the circuit *without* repeatedly waking modules.
- Common culprits: glovebox/trunk lights, door modules, radio amps, aftermarket alarms, stuck relays.

**CTA:**
(Use CTA Block C)

---

## Template 8 — “A/C not cold”
**Clarifying questions:**
1) Does the compressor clutch engage (or variable compressor command), and do radiator fans run with A/C on?
2) What are the ambient temp and vent temp, and is it worse at idle?
3) Any recent A/C service or signs of leaks (oily residue at fittings)?

**Safe diagnostic steps:**
- Start with airflow: cabin filter, condenser blocked with debris, fans working.
- If you have gauges: note high/low pressures; compare to expected for ambient.
- Do **not** recommend “topping off” without leak-checking—overcharge can hurt performance.
- UV dye/leak detection is often the right next step.

**CTA:**
(Use CTA Block A)

---

## Template 9 — “Rough idle / stalls at stops”
**Clarifying questions:**
1) Any codes (P0171/P0505/etc.)?
2) Does it change with A/C on, or after warm-up?
3) Has the throttle body/MAF been cleaned recently (and with what method)?

**Safe diagnostic steps:**
- Check for intake leaks and dirty throttle body (use the correct cleaner; avoid forcing electronic throttle plates).
- Review fuel trims at idle vs 2500 RPM to separate vacuum leaks from fuel delivery.
- If applicable, inspect PCV system and purge valve (stuck open purge can cause rough idle).

**CTA:**
(Use CTA Block B)

---

## Template 10 — “Brake/ABS warning light + safe approach”
**Clarifying questions:**
1) Which lights are on (ABS, traction, brake), and any stored ABS codes?
2) Any recent brake work, wheel bearing noise, or low brake fluid?
3) Does the issue happen after rain/snow or at certain speeds?

**Safe diagnostic steps:**
- Verify brake fluid level and look for leaks.
- Scan ABS module codes (generic OBD may not read them).
- Common: wheel speed sensor wiring damage or tone ring issues.
- If brake pedal feel is abnormal, avoid driving until inspected.

**CTA:**
(Use CTA Block A)

---

# 5 Fully-Written Example Answers (ready to post)

## Example 1 — P0300 Random/Multiple Misfire
A P0300 can be ignition, fuel, air, or even a mechanical issue—so the fastest path is to line up symptoms with data.

**A couple quick questions:**
1) What’s the **year/make/model/engine** and mileage? Any other codes besides P0300?
2) When does it act up most—**idle**, **under load**, **cold start**, or **hot**? Is the **CEL flashing**?
3) Do you have access to live data like **STFT/LTFT** and misfire counters?

**Safe checks you can do without guessing parts:**
- If the CEL is flashing, avoid hard driving until fixed (can damage the catalytic converter).
- Pop the engine cover (if equipped) and check:
  - Coil connectors fully seated, no broken locks
  - Plug wells dry (no oil/coolant)
  - Intake tube/clamps tight, no obvious vacuum hoses off
- If your scanner shows per-cylinder misfire counts, see if it’s truly “random” or if one cylinder is leading.
- If you end up with a specific cylinder (or you also have P0301–P0308):
  - Swap that cylinder’s **coil** with another cylinder and re-check if the misfire “follows.”
  - Same idea with the **spark plug** if plugs are serviceable and correctly gapped.
- If trims are very positive at idle (e.g., STFT/LTFT high +), that often points to an unmetered air/vacuum leak.

If you post freeze-frame + trims, it’ll be pretty easy to steer you toward ignition vs vacuum leak vs fuel delivery.

**Want a tailored test plan?**
Paste this into MadnessBot and it’ll structure the likely causes and next checks:

**Copy/paste prompt:**
```
Vehicle: [year make model engine]
Codes: P0300 (+ any others)
Symptoms: [idle/load/cold/hot], CEL flashing? [yes/no]
Freeze frame: [RPM, load, ECT]
Live data: STFT/LTFT at idle and 2500 RPM, misfire counters
Recent work: [plugs/coils/injectors/air filter]
```
Tracked link: **[MADNESSBOT_TRACKED_LINK]**

---

## Example 2 — P0420 Catalyst Efficiency Below Threshold
P0420 is often blamed on the catalytic converter, but the converter is frequently a *victim* of upstream problems. The goal is to confirm whether it’s an exhaust leak/sensor issue/mixture problem vs a worn cat.

**Quick questions:**
1) Any other codes (especially **misfire**, **P0171/P0172**, or O2 sensor codes) before P0420?
2) Any exhaust work lately or do you hear a cold-start **ticking** that quiets down (possible leak)?
3) What’s the mileage, and is it burning oil or losing coolant?

**Safe diagnostic steps:**
- Fix any misfire or fuel-trim codes first. A cat code after a misfire is common.
- Inspect for **exhaust leaks upstream of the rear O2** (manifold, flex pipe, flange gaskets). Even a small leak can skew readings.
- Use live data:
  - Upstream O2/AFR should switch/respond quickly.
  - Downstream O2 should be comparatively steadier if the cat is storing oxygen properly.
- If you can, check fuel trims at cruise. A chronically rich/lean condition can trigger P0420.

If you share O2 graphs or at least sensor voltages/AFR and trims, we can avoid throwing a converter at it unnecessarily.

**If you want, MadnessBot can interpret your O2 + trim data and suggest the next best check:**

**Copy/paste prompt:**
```
Vehicle: [year make model engine]
Code: P0420
Other codes: [list]
Mileage: [miles]
Symptoms: [none / power loss / smell]
Live data: upstream O2/AFR behavior, downstream O2 behavior, STFT/LTFT at cruise
Exhaust leaks? [yes/no/unknown]
```
Tracked link: **[MADNESSBOT_TRACKED_LINK]**

---

## Example 3 — No-Crank (single click / rapid clicks / nothing)
No-crank is usually a battery/connection issue, a starter/relay issue, or a control issue (park/neutral switch, immobilizer). The “sound” it makes matters a lot.

**A few clarifying questions:**
1) When you turn the key: **no sound**, **single click**, or **rapid clicking**?
2) What’s battery voltage **at rest** and what does it drop to **during a crank attempt**?
3) Any security/immobilizer light flashing, or did this start after any repairs?

**Safe step-by-step checks:**
- Check battery terminals: clean, tight, and check the **ground strap** where it bolts to body/engine.
- Turn headlights on and try to crank:
  - If lights go very dim → likely weak battery or high resistance connection.
  - If lights stay bright and nothing happens → likely control circuit (relay/ignition switch/neutral safety) or starter.
- If you can jump it from a known-good vehicle/jump pack, note whether behavior changes.
- Verify starter/IGN fuses and starter relay (some relays can be swapped with an identical one in the fuse box for testing).

Avoid “screwdriver jumping” at the starter on the forum—too many ways to short things or bypass safety.

**If you paste your voltage readings, MadnessBot can map them to likely failure points:**

**Copy/paste prompt:**
```
Vehicle: [year make model engine]
No-crank behavior: [no sound/single click/rapid clicks]
Battery age: [years]
Voltage: resting [V], key on [V], during crank attempt [V]
Jump start result: [no change / starts]
Dash lights/security light behavior: [details]
Recent work: [details]
```
Tracked link: **[MADNESSBOT_TRACKED_LINK]**

---

## Example 4 — Overheating (idle vs highway)
Overheating can turn expensive quickly, so the safe approach is: confirm coolant level, find leaks, verify fan/thermostat behavior, and avoid running it hot.

**Questions to narrow it down:**
1) Does it overheat mainly at **idle**, **highway speeds**, or both?
2) Are you losing coolant (and if so, how often are you topping off)? Any puddles/smell?
3) Does the heater blow **hot** when the gauge starts climbing?

**Safe diagnostic steps:**
- Don’t open the cap when hot—let it cool completely.
- When cold, verify the radiator and reservoir levels (some cars have a separate bleed procedure).
- Inspect for external leaks: radiator end tanks, hose connections, thermostat housing, and water pump weep hole.
- Check fan operation:
  - With A/C on, many vehicles command the fans; if fans never come on, suspect fan circuit or coolant temp sensor data.
- If it overheats at highway but not idle: think restricted radiator flow or low coolant.
- If it overheats at idle but not highway: think fans, airflow, or coolant circulation at low RPM.

If you can share ambient temp, what the coolant temp reaches (from scanner if available), and whether the upper/lower radiator hoses get hot, that helps a lot.

**Want a structured plan based on your exact symptoms?**

**Copy/paste prompt:**
```
Vehicle: [year make model engine]
Overheats: [idle/highway/both]
Coolant loss: [none/small/large] + where seen
Heater output when hot: [hot/lukewarm/cold]
Fans: [on/off/unknown] with A/C on
Temps: [gauge position or ECT °F/°C from scanner]
Recent work: [thermostat/water pump/radiator]
```
Tracked link: **[MADNESSBOT_TRACKED_LINK]**

---

## Example 5 — Parasitic Draw (battery dead overnight)
If the battery is going dead overnight, the trick is to separate **battery health** from **excess key-off draw**, then isolate the circuit without waking modules constantly.

**A few questions:**
1) Battery age and has it been load-tested (or tested at a parts store)?
2) How fast does it die (overnight vs 2–3 days)?
3) Any aftermarket gear (alarm, remote start, amps, dash cam), or did this start after a repair?

**Safe diagnostic steps:**
- First confirm charging voltage while running (many cars are ~13.8–14.7V, varies). If charging is low, fix that before chasing draw.
- For parasitic draw testing:
  - Turn everything off, close doors (latch them if needed), and wait for modules to sleep (can be 15–45 minutes).
  - Use a multimeter **in series** on the battery negative cable (or a DC clamp meter if available).
  - Typical key-off draw is often tens of milliamps; exact spec varies by car.
- If draw is high, pull fuses **one at a time** and watch for a big drop; note which fuse changes it.
- Common culprits: glovebox/trunk light stuck on, door module staying awake, radio/amp, stuck relay, aftermarket accessories.

If you tell me the measured asleep current and which fuse drops it, we can usually pinpoint the subsystem quickly.

**If you want MadnessBot to guide the fuse-pull workflow and interpret your readings:**

**Copy/paste prompt:**
```
Vehicle: [year make model]
Battery age/test result: [details]
Time-to-dead: [hours/days]
Charging voltage running: [V]
Parasitic draw: before sleep [mA], after sleep [mA]
Fuse pull results: [fuse name -> new mA]
Aftermarket equipment: [list]
```
Tracked link: **[MADNESSBOT_TRACKED_LINK]**

---

## Optional: Signature line (use sparingly)
*I’m not a mechanic—just trying to help you diagnose it systematically and safely.*

---

## Quick customization checklist
- Replace: **[year make model engine]**, **[MADNESSBOT_TRACKED_LINK]**
- Remove any steps you’re not confident about for that platform’s audience.
- Keep it short enough that it doesn’t look like marketing.
