# Starbook Agent Handoff / 蹇呰鍏ュ彛

> **杩欐槸鎵€鏈夋柊 Agent銆丄I 缂栫▼绐楀彛鍜屾柊寮€鍙戜細璇濈殑绗竴鍏ュ彛銆?*
>
> 鍦ㄤ慨鏀逛换浣曚唬鐮併€佹暟鎹簱銆侀儴缃查厤缃垨浜у搧浣撻獙涔嬪墠锛屽繀椤诲厛瀹屾垚鏈枃瑙勫畾鐨勯槄璇婚『搴忋€備笉瑕佷粎鍑棫瀵硅瘽銆佹枃浠跺悕鎴栧眬閮ㄤ唬鐮佺寽娴嬪綋鍓嶆灦鏋勩€?

## 1. 褰撳墠椤圭洰韬唤

- Project: **Starbook / 鏄熷笨涔嬩功**
- Current version: **1.7.1**
- Production branch: **`main`**
- Production deploy: **GitHub Pages via GitHub Actions**
- Runtime backend: **Supabase Anniversary Bridge**
- Current Book: **鏄熷笨涔嬩功** (`8a3cc6fe-b667-4ce7-b47b-79cebc0e1353`)
- Current product preset:
  - relationship: `romantic`
  - theme: `magic-celestial`
  - experience: `world-map`
- Current delivery priority: **2026-10-29 鍛ㄥ勾绾康鐗堢ǔ瀹氫氦浠?*

## 2. Agent 蹇呰椤哄簭

浠讳綍鏂?Agent 鍦ㄥ紑濮嬪伐浣滃墠锛屾寜椤哄簭闃呰锛?

1. `AGENTS.md` 鈥斺€?褰撳墠鏂囦欢锛岀‘璁ゅ崗浣滆鍒欍€?
2. `PROJECT_STATE.md` 鈥斺€?褰撳墠鐪熷疄鐘舵€併€佹妧鏈€恒€佸凡楠岃瘉鑳藉姏銆佷笅涓€浼樺厛绾с€?
3. `docs/PROJECT_MANAGEMENT_FULL_CHAIN.md` 鈥斺€?椤圭洰绠＄悊銆佸紑鍙戙€佸彂甯冦€侀儴缃层€佹暟鎹€佸洖婊氬叏閾捐矾銆?
4. `docs/ARCHITECTURE_EXTENSION_CONTRACT.md` 鈥斺€?褰撳墠鏋舵瀯杈圭晫涓庢湭鏉ユ墿灞曚笉鍙牬鍧忕害鏉熴€?
5. `docs/DATA_LIFECYCLE.md` 鈥斺€?Supabase 鏁版嵁鐢熷懡鍛ㄦ湡銆佺増鏈崌绾т笌杩佺Щ瑙勫垯銆?
6. `CHANGELOG.md` 鈥斺€?宸插畬鎴愮殑鐗堟湰鍙樺寲銆?
7. `ROADMAP.md` 鈥斺€?鏈畬鎴愪簨椤瑰拰鍚庣画鏂瑰悜銆?
8. 褰撳墠鐩爣鐗堟湰瀵瑰簲 `docs/releases/vX.X.X.md`銆?
9. 鏈€鍚庢墠璇诲彇涓庝换鍔＄洿鎺ョ浉鍏崇殑婧愪唬鐮併€?

濡傛灉涓婅堪鏂囦欢涓庢棫鑱婂ぉ璁板綍鍐茬獊锛?*浠ヤ粨搴撳綋鍓嶆枃浠朵负鍑?*銆?

## 3. 淇敼鍓嶅繀椤诲洖绛旂殑 7 涓棶棰?

Agent 鍦ㄥ姩鎵嬪墠搴旇嚜琛岀‘璁わ細

1. 褰撳墠瑕佷慨鏀圭殑鏄摢涓€涓増鏈紵
2. 杩欐鏀瑰姩灞炰簬浜у搧鍔熻兘銆佺ǔ瀹氭€с€佹灦鏋勩€佹暟鎹€侀儴缃茶繕鏄枃妗ｆ不鐞嗭紵
3. 鏄惁褰卞搷 `SB.user / SB.book / SB.magicBook / SB.theme / SB.experience / SB.store` 鐨勮亴璐ｈ竟鐣岋紵
4. 鏄惁褰卞搷 Supabase schema銆丷LS銆丼torage 鎴栫幇鏈夌湡瀹炴暟鎹紵
5. 鏄惁褰卞搷 GitHub Actions銆佸垎鏀€丳R銆乵ain 鎴?Pages锛?
6. 鏄惁鐮村潖澶氱敤鎴枫€佸 Book銆佸鍏崇郴銆佸 Theme銆佸 Experience 鐨勬湭鏉ュ吋瀹规€э紵
7. 鏈鏀瑰姩闇€瑕佸悓姝ユ洿鏂板摢浜涚増鏈褰曪紵

濡傛灉涓嶈兘鍥炵瓟锛屼笉搴旂洿鎺ュぇ瑙勬ā閲嶆瀯銆?

## 4. 褰撳墠鏈€閲嶈鐨勬灦鏋勮竟鐣?

- `SB.book` = **褰撳墠鏁版嵁 Book / Book Context**锛屼笉寰楀啀鐢ㄤ簬榄旀硶涔﹁瑙夋帶鍒躲€?
- `SB.magicBook` = **Magic Celestial 榄旀硶涔﹁瑙変笌寮€涔﹀姩鐢绘帶鍒跺櫒**銆?
- `SB.store` = **涓氬姟鏁版嵁鍏煎灞?*锛屽綋鍓嶅唴閮ㄨ鍐?Supabase `book_data.payload`銆?
- `magic-celestial` 鍙槸绗竴濂?Theme锛屼笉绛変簬 Starbook Core銆?
- `world-map` 鍙槸绗竴濂?Experience锛屼笉绛変簬 Starbook Core銆?
- 褰撳墠鏄儏渚ｄ功锛屼絾 Starbook Core 涓嶅緱鍐欐鈥滄儏渚ｆ槸鍞竴鍏崇郴鈥濄€?
- 褰撳墠 UI 鍙湁涓€鏈?Book锛屼絾涓氬姟浠ｇ爜涓嶅緱鍋囪鐢ㄦ埛姘歌繙鍙湁涓€鏈?Book銆?
- 褰撳墠 Memory 涓?City 浠嶆湁 V1 鑰﹀悎锛岃繖鏄妧鏈€猴紝涓嶅簲杩涗竴姝ュ己鍖栥€?

## 5. 褰撳墠鏁版嵁涓庡彂甯冨師鍒?

### 浠ｇ爜鐢熷懡鍛ㄦ湡

`release/*` 鎴?`feature/*` 鈫?PR 鈫?`validate-starbook` 鈫?merge `main` 鈫?GitHub Pages 鑷姩閮ㄧ讲銆?

### 鏁版嵁鐢熷懡鍛ㄦ湡

Supabase Database / Private Storage **鐙珛浜?Git 鍒嗘敮鍜?Pages 閮ㄧ讲**銆?

姝ｅ父鍓嶇鐗堟湰鍗囩骇锛?

- 涓嶆竻绌?Supabase锛?
- 涓嶉噸鏂?seed Book锛?
- 涓嶉噸鏂板鍏ョ収鐗囷紱
- 涓嶉噸鏂板鍏ュ洖蹇嗭紱
- 涓嶆墽琛岀牬鍧忔€?reset SQL銆?

鏁版嵁搴撶粨鏋勫崌绾ф垨 Production 鏁版嵁鍏冧俊鎭?鎴愬憳鍙樻洿蹇呴』浣跨敤**鍚戝墠 migration**銆?

褰撳墠 v1.5.1 鐨勬爣棰樹笌鎴愬憳鍙樻洿鐢?`supabase/migrations/002_v151_title_and_members.sql` 绠＄悊锛岀姝㈤€氳繃閲嶈窇 seed 娓呯┖鎴栬鐩栦笟鍔℃暟鎹€?

## 6. 姣忎釜鐗堟湰寮哄埗缁存姢鐨勬枃浠?

姣忎釜姝ｅ紡鐗堟湰蹇呴』鍚屾鏇存柊锛?

- `VERSION`
- `CHANGELOG.md`
- `ROADMAP.md`
- `PROJECT_STATE.md`
- `docs/releases/vX.X.X.md`

濡傛灉椤圭洰绠＄悊閾捐矾銆佹灦鏋勮竟鐣屻€佹暟鎹瓥鐣ユ垨鍙戝竷绛栫暐鍙樺寲锛岃繕蹇呴』鍚屾鏇存柊锛?

- `AGENTS.md`
- `docs/PROJECT_MANAGEMENT_FULL_CHAIN.md`
- `docs/ARCHITECTURE_EXTENSION_CONTRACT.md`
- `docs/DATA_LIFECYCLE.md`
- `docs/RELEASE_WORKFLOW.md`

`tools/check_project.py` 涓?`validate-starbook` 浼氭鏌ュ叾涓竴閮ㄥ垎瑕佹眰銆?

## 7. 姣忎釜 Release Record 蹇呴』鏄庣‘鍐欏嚭鐨勯摼璺彉鍖?

姣忎釜 `docs/releases/vX.X.X.md` 鑷冲皯鍖呭惈锛?

- 鏈増鐩爣锛?
- 浜у搧浣撻獙鍙樺寲锛?
- Runtime / 鏋舵瀯閾捐矾鍙樺寲锛?
- 鏁版嵁閾捐矾鍙樺寲锛?
- Auth / 鏉冮檺 / RLS 鍙樺寲锛?
- Storage 鍙樺寲锛?
- Git / PR / CI / Pages 鍙戝竷閾捐矾鍙樺寲锛?
- Agent / 鏂囨。娌荤悊閾捐矾鍙樺寲锛?
- 鏂囦欢鍙樺寲锛?
- Migration / 鎵嬪姩鎿嶄綔锛?
- 娴嬭瘯涓庨獙璇侊紱
- 宸茬煡闂锛?
- 鍥炴粴鏂瑰紡锛?
- 涓嬩竴鐗堟湰寤鸿銆?

濡傛灉鏌愪竴椤规病鏈夊彉鍖栵紝涔熷繀椤绘槑纭啓鈥滄棤鍙樺寲鈥濓紝涓嶈兘鐪佺暐銆?

## 8. 鍙戝竷鍓嶆渶浣庢鏌?

鑷冲皯鎵ц锛?

```powershell
python build.py
python tools/check_project.py
```

鐒跺悗閫氳繃 PR 鐨?`validate-starbook`銆?

姝ｅ紡 Pages 鍙厑璁?`main` 閮ㄧ讲銆?

## 9. 绂佹浜嬮」

闄ら潪鐢ㄦ埛鏄庣‘鎵瑰噯骞跺凡鏈夎縼绉?鍥炴粴鏂规锛屽惁鍒欑姝細

- 閲嶇疆 Supabase production 鏁版嵁锛?
- 鍒犻櫎鐪熷疄 `book_data` / Storage 鏂囦欢锛?
- 閲嶆柊杩愯浼氳鐩栫湡瀹炴暟鎹殑 seed锛?
- 鍦ㄥ墠绔垨浠撳簱鍔犲叆 `sb_secret_`銆乣service_role`銆佹暟鎹簱瀵嗙爜銆丟itHub PAT锛?
- 鍏抽棴 RLS 鏉モ€滆В鍐斥€濇潈闄愰敊璇紱
- 缁曡繃 `main` 鐩存帴璁?release/feature 鍒嗘敮瑕嗙洊 Production锛?
- 鏃犵増鏈褰曞湴淇敼 schema锛?
- 涓轰簡閲嶆瀯婕備寒鑰岀牬鍧?2026-10-29 鍛ㄥ勾浜や粯绋冲畾鎬э紱
- 鎶?`SB.book` 涓?`SB.magicBook` 鍐嶆鍚堝苟锛?
- 灏嗗綋鍓嶅敮涓€ Theme / Experience / Relationship 鍐欐涓哄钩鍙板敮涓€鑳藉姏銆?

## 10. Agent 浜ゆ帴杈撳嚭鏍煎紡

涓€涓?Agent 瀹屾垚宸ヤ綔鍚庯紝搴斿湪鍥炲鎴?release record 涓鏄庯細

1. 褰撳墠鐗堟湰锛?
2. 瀹屾垚浜嗕粈涔堬紱
3. 淇敼/鏂板/鍒犻櫎浜嗗摢浜涙枃浠讹紱
4. 鏄惁鏀规暟鎹簱锛?
5. 鏄惁闇€瑕佺敤鎴锋墜鍔ㄦ搷浣滐紱
6. 濡備綍娴嬭瘯锛?
7. 鏄惁褰卞搷 Production / Supabase 鏁版嵁锛?
8. 宸茬煡闂锛?
9. 涓嬩竴姝ュ缓璁紱
10. 鏄惁宸茬粡鏇存柊鐗堟湰娌荤悊鏂囨。銆?

---

**鏍稿績鍘熷垯锛歋tarbook 鐨勪唬鐮佸彲浠ヨ凯浠ｏ紝鐢ㄦ埛鐪熷疄鍥炲繂鏁版嵁蹇呴』鎸佺画瀛樺湪锛涘綋鍓嶅懆骞寸増鏈彲浠ョ畝鍗曪紝浣嗘湭鏉ユ墿灞曟帴鍙ｄ笉鑳借鍐欐銆?*

## 11. 涓€閿彂甯冨叆鍙?

鐗堟湰寮€鍙戝畬鎴愬悗锛屼笉鍐嶈姹?Owner/Agent 姣忔閲嶆柊鎷兼帴 Git 鍙戝竷鍛戒护銆傞閫夊叆鍙ｏ細

```powershell
.\release-current.ps1
```

瑙勫垯锛?

- 鐗堟湰鍙峰敮涓€鏉ユ簮鏄牴鐩綍 `VERSION`锛?
- 鑴氭湰鑷姩鐢熸垚缂哄け鐨?`docs/releases/vX.X.X.md` 鍩虹璁板綍锛屼絾 Agent 浠嶈礋璐ｈˉ鍏ㄧ湡瀹為摼璺彉鍖栵紱
- 鑴氭湰鑷姩鐢熸垚 `scripts/releases/release-vX.X.X.ps1` 浣滀负鐗堟湰瀹¤璁板綍锛?
- `publish.ps1` 浠嶆槸搴曞眰鍙戝竷鎵ц鍣紝涓嶅缓璁柊 Agent鍙﹂€犲彂甯冩祦绋嬶紱
- 鏁版嵁搴?migration 缁濅笉鐢卞彂甯冭剼鏈嚜鍔ㄦ墽琛屻€?

瀹屾暣璇存槑锛歚docs/RELEASE_AUTOMATION.md`銆?
