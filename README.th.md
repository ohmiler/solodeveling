# Solodeveling

[English](README.md) | [ภาษาไทย](README.th.md)

> **เอเจนต์เดียว กระบวนการเท่าที่จำเป็น ตั้งแต่งานแก้เล็ก ๆ จนถึง release ที่ตรวจสอบแล้ว**

Solodeveling คือโปรโตคอลส่งมอบซอฟต์แวร์แบบ single-agent-first สำหรับนักพัฒนาเดี่ยว
โดยช่วยให้เอเจนต์หลักหนึ่งตัวรักษาทิศทางของงานตั้งแต่การสำรวจ วางแผน ลงมือทำ
ตรวจสอบ ความปลอดภัย release และ maintenance งานเล็กที่ปลอดภัยสามารถทำแบบ
ephemeral ได้ ส่วนงานที่ต้องกลับมาทำต่อหรือมีความเสี่ยงจะเพิ่ม memory และ gate
ที่เข้มขึ้นเท่าที่ความเสี่ยงนั้นสมควรได้รับ

ใช้ชุด skill มาตรฐานเดียวกันได้กับ Codex, Claude Code, Cursor และ client ที่รองรับ
Agent Skills แม้จะใช้ subagent ได้เมื่อมีประโยชน์ แต่ Solodeveling ไม่บังคับให้มีทีม
หลายเอเจนต์สำหรับ workflow ทั่วไป

**สถานะ:** รุ่น Alpha เผยแพร่ผ่าน
[npm](https://www.npmjs.com/package/solodeveling),
[PyPI](https://pypi.org/project/solodeveling/) และ
[GitHub Release แบบ immutable](https://github.com/ohmiler/solodeveling/releases/latest)
Codex และ Claude Code ผ่าน representative live scenario แบบจำกัดขอบเขตอย่างละหนึ่งกรณี
ส่วน Cursor มีเฉพาะหลักฐานเชิงโครงสร้างของ adapter เพราะไม่พบ `cursor-agent`
สถานะ Tier 1 จึงยังไม่ผ่านการยืนยันจนกว่า core scenario matrix ทั้งชุดจะผ่าน

## เริ่มต้นใช้งานอย่างรวดเร็ว

ผู้ใช้ Node.js ใช้เพียงคำสั่งเดียว:

~~~console
npx solodeveling install
~~~

หากต้องการติดตั้งคำสั่งแบบถาวร:

~~~console
npm install -g solodeveling
solodeveling install
~~~

ผู้ใช้ Python สามารถเรียกใช้โดยไม่ติดตั้งถาวร หรือติดตั้งเป็น tool ได้ดังนี้:

~~~console
uvx solodeveling install
uv tool install solodeveling
pipx install solodeveling
~~~

ทุกช่องทางมีคำสั่งสาธารณะเพียงชื่อเดียวคือ `solodeveling` อ่านข้อกำหนดเบื้องต้น
แพลตฟอร์มที่รองรับ วิธีอัปเกรด และ integrity controls ได้ที่
[การติดตั้ง](docs/installation.md)

## ทำไมต้อง Solodeveling

- **Single-agent-first:** มีเอเจนต์หลักหนึ่งตัวที่รับผิดชอบงาน แทนการบังคับแบ่งบทบาท
  ส่งต่องาน หรือทำงานแบบขนานในทุกครั้ง
- **เงียบเมื่องานเล็ก:** งาน Quick ที่ปลอดภัยไม่จำเป็นต้องถามคำถาม เขียน project memory
  หรือใช้การตรวจสอบเกินสัดส่วนของผลกระทบ
- **ตรงไปตรงมาสำหรับงานอ่านอย่างเดียว:** Q&A, คำอธิบาย, review, status, diagnosis
  และคำแนะนำในบทสนทนา จะอ่านเฉพาะสิ่งที่จำเป็นต่อข้อสรุปและไม่สร้าง lifecycle artifact
- **คงทนเมื่อจำเป็น:** งานที่ต้องกลับมาทำต่อจะบันทึกสถานะปัจจุบัน ส่วนงาน Critical
  จะเพิ่มขอบเขตด้านความปลอดภัย recovery หลักฐาน และ release อย่างชัดเจน
- **ครอบคลุมวงจรส่งมอบ:** ใช้คำศัพท์ชุดเดียวตั้งแต่ discovery, coding และ debugging
  ไปจนถึง verification, release และ maintenance
- **อยู่ในโปรเจกต์และพกพาได้:** ติดตั้ง skill เดียวกันลงใน runtime ที่ตรวจพบใน repository
  โดยไม่ค้นหาหรือแก้ installation ส่วนกลางของเอเจนต์

| ระดับงาน | พฤติกรรมเริ่มต้น | ภาระที่ต้องเก็บถาวร |
| --- | --- | --- |
| Direct Read-Only | ตอบหรือสำรวจภายในสิทธิ์แบบไม่แก้ไขที่ผู้ใช้ให้มา | ไม่มี |
| Quick | ลงมือทันทีเมื่อเจตนาชัดเจน และยกระดับเมื่อพบความเสี่ยง | งาน ephemeral ที่ปลอดภัยไม่ต้องเก็บ |
| Standard | ทำงานที่ชัดเจนผ่าน workflow เดียวตั้งแต่กำหนดรูป → วางแผน → ลงมือ → ตรวจสอบ และแยก workflow เมื่อมี boundary จริง | WORK แบบกระชับหนึ่งไฟล์และ EVIDENCE สะสมหนึ่งไฟล์ |
| Critical | เพิ่ม security, recovery, provenance และ authorization gate ที่ชัดเจน | บันทึกงานและหลักฐานที่ตรวจสอบย้อนหลังได้ |

งานต่อเนื่องขนาดจำกัดภายใน session เดียวจะใช้ Ephemeral Quick ก่อนเปิดหรือ reuse งาน
Standard เดิม ให้ reuse คู่ Standard เฉพาะเมื่อความต่อเนื่องต้องข้าม session มีการเปลี่ยน
durable decision หรือยังอยู่ใน batch ที่ goal, acceptance, authority, risk, release boundary
และ rollback ไม่เปลี่ยนแปลง Roadmap จะอัปเดตเฉพาะเมื่อ priority, milestone, ลำดับงาน
หรือการตัดสินใจเลื่อนงานเปลี่ยนไป WORK เป็นเจ้าของ scope และ decision ส่วน EVIDENCE
เป็นเจ้าของ checks และ limitations โดย state เก็บเฉพาะบริบทที่จำเป็นต่อการทำงานต่อ

สำหรับ Standard ที่ทำต่อเนื่องใน session เดียว จะ persist `active` ครั้งเดียว แล้วเขียน
หลักฐานสุดท้ายพร้อม `done` และ archive ครั้งเดียวหลัง verification สถานะระหว่างทางจะ
persist เฉพาะเมื่อต้องข้าม session, มี blocker, ต้อง handoff, scope/risk เปลี่ยน หรือผู้ใช้
ขอ checkpoint หลักฐาน automation ที่ยังครอบคลุมอยู่จะ reuse ตามขอบเขตจริง และ manual
browser review จะตรวจเฉพาะคุณภาพภาพหรือ interaction ที่ automation ยังไม่พิสูจน์

Backend query และ API handler ยังคงเป็น Standard โดยปริยาย งาน mapping, sorting, copy
หรือ refactor ที่ให้ผลเท่าเดิมและเป็น read-only อาจคงเป็น Quick ได้เฉพาะเมื่อ access,
ข้อมูล sensitive, validation, response compatibility, ข้อมูลที่บันทึก และ external effect
ไม่เปลี่ยน พร้อม focused contract test ที่พิสูจน์ boundary นั้น หากมีความไม่แน่ใจให้คง
เป็น Standard

### เมื่อใช้และไม่ใช้ Solodeveling

coding agent สามารถเขียน `TODO.md` หรือบันทึกสิ่งที่ต้องทำใน session ถัดไปได้โดยไม่ต้อง
ติดตั้ง skill ใด Solodeveling ไม่ได้ทำให้โมเดลฉลาดขึ้นโดยตรง แต่บรรจุกติกาการส่งมอบที่ใช้ซ้ำได้
เพื่อให้ผู้ใช้ไม่ต้องสร้างวิธีทำงานขึ้นใหม่ในทุก prompt หรือทุก session

| ประเด็น | เมื่อไม่มี skill ร่วม | เมื่อใช้ Solodeveling |
| --- | --- | --- |
| การประสานงาน | คำสั่งและวิธีทำงานขึ้นอยู่กับ prompt, agent และ session ปัจจุบัน | skill ที่ติดตั้งในโปรเจกต์ให้ routing และคำศัพท์ชุดเดียวกันบน runtime ที่รองรับ |
| ความต่อเนื่อง | ผู้ใช้หรือ agent เลือกรูปแบบการจดบันทึกได้อย่างอิสระ | state แบบกระชับเก็บเฉพาะบริบทที่ต้องใช้ทำงานต่อ และข้อมูลถาวรแต่ละชนิดมีเจ้าของเพียงแห่งเดียว |
| งานเล็ก | แทบไม่มีพิธีการได้หาก agent ตัดสินใจเหมาะสม | Direct Read-Only และ Ephemeral Quick ระบุชัดว่าไม่ต้องสร้าง lifecycle artifact |
| การยืนยันว่าเสร็จ | prompt หรือ session เป็นตัวกำหนดว่าหลักฐานเท่าใดจึงเพียงพอ | การกล่าวอ้างว่าเสร็จต้องมี verification ล่าสุดที่ตรงกับขอบเขตซึ่งเปลี่ยนไป |
| งานเสี่ยง | ต้องระบุ security, authority, recovery และ release checks ผ่าน prompt หรือกระบวนการอื่น | งาน Critical ใช้ security, recovery, provenance และ authorization gate ที่ชัดเจน |

ไม่ใช่ทุกโปรเจกต์ที่จำเป็นต้องใช้ Solodeveling โปรเจกต์เล็ก ความเสี่ยงต่ำ และจบใน session เดียว
อาจเหมาะกับ prompt ที่ชัดเจนและ `TODO.md` มากกว่า Solodeveling จะคุ้มกับ overhead เมื่อการตัดสินใจ
ต้องทำซ้ำ งานต้องต่อข้าม session หรือจำเป็นต้องตรวจสอบตามระดับความเสี่ยง ข้อกล่าวอ้างที่ทดสอบได้
จึงไม่ใช่ว่า skill ทำให้โมเดลฉลาดขึ้น แต่เป็น shared protocol ที่ลดการประสานงานซ้ำและลด gate
ที่ตกหล่นโดยไม่เพิ่มภาระให้งานเล็ก

## เปรียบเทียบกับแนวทางอื่น

โครงการเหล่านี้มีค่าเริ่มต้นต่างกัน ไม่มีแนวทางใดชนะทุกกรณี ตารางนี้สรุปเอกสารสาธารณะ
ณ เดือนกรกฎาคม 2026 และไม่ใช่ benchmark ด้านความเร็วหรือคุณภาพแบบควบคุมตัวแปร

| โครงการ | ค่าเริ่มต้นที่เอกสารระบุ | เหมาะที่สุดกับ | จุดต่างหลักจาก Solodeveling |
| --- | --- | --- | --- |
| **Solodeveling** | เอเจนต์หลักหนึ่งตัว พร้อม workflow และ memory ตามระดับความเสี่ยง | ผู้ดูแลโปรเจกต์เดี่ยวที่ต้องสมดุลงานเล็กกับ security, release และ maintenance | งาน Quick ทำแบบ ephemeral ได้ และเพิ่มหลักฐานที่ audit ได้เมื่อจำเป็น |
| [Superpowers](https://github.com/obra/superpowers) | วิธีพัฒนาที่ประกอบจาก skill หลายชิ้น | ผู้ที่ต้องการ skill ด้านวิศวกรรม การวางแผน review และเส้นทางแบบ subagent เมื่อรองรับ | Solodeveling ใช้เอเจนต์หลักที่รับผิดชอบเป็นค่าเริ่มต้นและไม่บังคับ delegation |
| [GSD](https://github.com/gsd-build/get-shit-done) | Lightweight meta-prompting, context engineering และ spec-driven execution | งานยาวที่ต้องรับมือกับ context degradation เป็นหลัก | Solodeveling จัด persistence และ verification ตามความเสี่ยงตลอด delivery lifecycle |
| [GitHub Spec Kit](https://github.github.com/spec-kit/) | Specification-centered flow: Spec, Plan, Tasks, Implement | งานที่ต้องให้ specification เป็น source of truth หลักในหลาย integration | Solodeveling อนุญาตให้งาน Quick ที่ปลอดภัยไม่ต้องมี persistent spec แต่ยังยกระดับได้ |
| [BMAD Method](https://github.com/bmad-code-org/BMAD-METHOD) | Agile workflow ที่ปรับตามขนาด พร้อมบทบาทเฉพาะทางมากกว่า 12 บทบาทและ workflow มากกว่า 34 แบบ | ผู้ที่ต้องการ persona, module และระบบ agile workflow ขนาดใหญ่ | Solodeveling เลือกเอเจนต์หลักหนึ่งตัวและคำศัพท์ร่วมชุดเล็กตลอด lifecycle |

### คำว่าเร็วกว่าในที่นี้หมายถึงอะไร

Solodeveling ลด **workflow overhead** ไม่ได้อ้างว่าเพิ่มความฉลาดของโมเดล และยังไม่อ้างว่า
ทำ coding task เสร็จเร็วกว่าแนวทางข้างต้น การกล่าวอ้างอย่างเป็นธรรมต้องใช้ repository,
model, prompt, ชุดงาน และจำนวนรอบที่เท่ากัน Repository นี้มี
[แผน pilot เปรียบเทียบ Solodeveling/Superpowers จำนวน 18 runs](docs/comparative-benchmark.md)
พร้อม source/runtime pins, hidden correctness checks, offline planning และ live-authorization
gate แยกต่างหาก Pilot 1 ล้มเหลวก่อน inference, Pilot 2 ไม่ได้ activate methodology ใด
และ Pilot 3 แก้ไฟล์ไม่ได้เพราะ Windows sandbox ขัดข้อง ทั้งหมดจึงเป็น measurement run
ที่ใช้ไม่ได้ ไม่ใช่ผลการเปรียบเทียบ นอกจากนี้
[แผนการวัดผลจาก feedback](docs/measurement.md) ได้ preregister pilot เปรียบเทียบ
0.1.1 กับ 0.1.2 แบบ correctness-gated และ field scorecard จำนวนยี่สิบงานไว้แล้ว
แผนเดียวกันยังเพิ่มการเปรียบเทียบ 30 calls ที่ยังไม่ได้รัน ระหว่าง Solodeveling
0.2.0 ที่ pin ไว้กับแขนที่ไม่ใช้ skill จริง ครอบคลุมงาน read-only, Quick, Standard,
งานต่อเนื่อง และการประเมินความพร้อมระดับ Critical โดยยึด correctness ก่อน
preregistration เป็นเพียงแผนทดสอบ ไม่ใช่ผลบวกหรือคำกล่าวอ้างด้านประสิทธิภาพต่อสาธารณะ

| หลักฐานจาก repository นี้ | ผลที่สังเกตได้ | สิ่งที่หลักฐานรองรับ |
| --- | --- | --- |
| Ephemeral documentation dogfood | ไม่ถามผู้ใช้และไม่สร้าง memory artifact สำหรับงาน Quick | งานเล็กที่ชัดเจนลดพิธีการด้าน coordination และ persistence ได้ |
| Memory-only GitHub CI | Focused validation jobs เสร็จใน 18–20 วินาที | การอัปเดต memory ไม่กระตุ้น package, native หรือ full test jobs |
| Docs-only GitHub CI | Python regression job เสร็จใน 23–33 วินาที | เอกสารยังมี verification ที่มีความหมายโดยไม่รัน cross-platform package matrix |
| Bounded live portability scenario | Codex และ Claude Code ได้คะแนน 1.0 ใน Quick scenario อย่างละหนึ่งกรณี | Canonical behavior ส่งต่อข้ามสอง runtime ที่ใช้ได้ แต่ยังไม่ยืนยัน Tier 1 |

ดูวิธีการและข้อจำกัดเพิ่มเติมได้ที่
[EVIDENCE-006](.solodeveling/evidence/EVIDENCE-006.md),
[EVIDENCE-019](.solodeveling/evidence/EVIDENCE-019.md) และ
[EVIDENCE-025](.solodeveling/evidence/EVIDENCE-025.md)

## เหมาะกับใคร

เลือก Solodeveling เมื่อคุณ:

- ดูแลโปรเจกต์คนเดียวหรือทำงานร่วมกับ coding agent หลักหนึ่งตัว
- ต้องการให้งานแก้เล็ก ๆ เบา แต่ยังมีวินัยเพียงพอสำหรับงานเสี่ยง
- ต้องการความต่อเนื่องข้าม session โดยไม่สร้างเอกสารสำหรับทุก action
- รับผิดชอบทั้ง implementation, release หรือ maintenance
- สลับใช้ Codex, Claude Code, Cursor หรือ Agent Skills client อื่น

แนวทางอื่นอาจเหมาะกว่า หากคุณต้องการ persona เฉพาะทางและ multi-agent coordination
เป็นค่าเริ่มต้น บังคับ formal specification สำหรับทุกการเปลี่ยนแปลง หรือต้องการ ecosystem
ที่เติบโตเต็มที่และมีฐานหลักฐานเชิงพฤติกรรมขนาดใหญ่กว่า

## การติดตั้งเข้าโปรเจกต์อัตโนมัติ

workflow ทั่วไปไม่ต้องใส่ option:

~~~console
solodeveling install
solodeveling check
solodeveling uninstall
~~~

Solodeveling จะ reuse installation ที่ตัวเองจัดการอยู่ก่อน หากยังไม่มี จะตรวจ directory
แบบ project-local ของ Codex/Agent Skills, Claude Code และ Cursor แล้วติดตั้งทุก runtime
ที่ไม่ซ้ำกัน หากไม่พบ marker จะใช้ path มาตรฐาน `.agents/skills` โดยไม่ค้นหา executable
ส่วนกลางหรือเขียนออกนอกโปรเจกต์ปัจจุบัน

ระหว่างติดตั้ง ระบบจะ validate skill suite, preflight ทุก target, ปฏิเสธ symlink และ
path traversal, ไม่ทับ unmanaged collision, copy แบบ atomic และบันทึก managed hashes
คำสั่ง check ตรวจไฟล์ที่หาย ถูกแก้ หรือเกินจากรายการ ส่วน uninstall ลบเฉพาะ managed file
ที่ไม่ถูกแก้ไขและไม่มีโหมด force-delete

หลังติดตั้งครั้งแรก ให้เริ่ม agent session ใหม่ แล้วเรียก `$solodeveling` ใน Codex,
`/solodeveling` ใน Claude Code หรือ Cursor หรือใช้วิธี invoke ที่ client อื่นกำหนด

### Overrides ขั้นสูง

ระบบ automation และ workspace ที่ไม่ปกติสามารถเลือก runtime หรือโปรเจกต์ได้โดยตรง
ส่วน `--dry-run` เป็น preview แบบไม่บังคับ:

~~~console
solodeveling install --runtime claude-code --project-root PATH
solodeveling install --runtime cursor --dry-run
~~~

## คำสั่งอื่น

เส้นทางติดตั้งตั้งใจให้สั้น ส่วน project memory, tracked-work helpers และ evaluation
ต้องเรียกใช้อย่างชัดเจน:

~~~console
solodeveling init
solodeveling validate .
solodeveling work evidence . WORK-033 --claim "Focused tests pass" --method "Automated test" --result passed --scope "Lifecycle helper"
solodeveling work transition . WORK-033 verifying
solodeveling work archive . WORK-033 --next-action "Select the next priority"
solodeveling eval probe
solodeveling version
~~~

work helper จะ validate memory ก่อนและหลังแต่ละ operation, ปฏิเสธ transition ที่ผิด
อัปเดต work กับ state พร้อมกัน และ rollback หากเขียนได้เพียงบางส่วน งาน Standard
จะ reuse evidence file โดยอัตโนมัติ ส่วนงาน audited ที่มีหลาย evidence file เลือกไฟล์ได้ด้วย
`--evidence-id`

Live evaluation อาจใช้โควตาหรือเครดิตของ model service โปรดอ่าน
[การประเมินผลข้ามเอเจนต์](docs/cross-agent-evaluation.md) ก่อนอนุญาตให้รันแบบ live

## ขอบเขตด้านความปลอดภัยและการรองรับ

npm launcher ไม่มี runtime dependency และไม่มี install lifecycle script เมื่อผู้ใช้เรียก
อย่างชัดเจน มันจะเลือก native artifact ที่ตรงกับเวอร์ชัน ดาวน์โหลดจาก GitHub Release
ที่ระบุเวอร์ชัน ตรวจ bundled size และ SHA-256 แล้ว cache และ execute โดยไม่ผ่าน shell
Windows, macOS และ Linux บน x64 และ arm64 จะเป็น release target หลัง CI build และ
native smoke test ผ่านเท่านั้น target ที่ไม่รองรับจะ fail closed พร้อมแสดงทางเลือกติดตั้ง
ด้วย Python tool

Solodeveling ใช้ verification ตามระดับความเสี่ยงและแนวทาง Secure SDLC แต่การติดตั้ง
ไม่ได้ทำให้โปรเจกต์ปลอดภัยหรือ compliant โดยอัตโนมัติ Hash ใช้ตรวจการเปลี่ยนแปลงของ byte
แต่ไม่ได้พิสูจน์ตัวตน publisher ด้วยตัวเอง ระบบไม่เก็บ telemetry และไม่รวม publishing
credential ใด ๆ

CI ปกติจะไม่สร้าง tag, GitHub Release, npm package หรือ PyPI package การเผยแพร่ภายนอก
ต้องอ้างอิง source revision ที่ผ่าน review และได้รับอนุญาตแยกต่างหากอย่างชัดเจน

## สัญญาอนุญาต

Apache-2.0 ดูรายละเอียดที่ [LICENSE](LICENSE)
