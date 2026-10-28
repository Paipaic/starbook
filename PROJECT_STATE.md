# Starbook Project State

## Current Release

- Version: `1.8.3` (寮€涔︺€屾満鍏冲惎灏併€嶏細鏈哄叧閫愮骇鍟悎銆佸疂鐭虫棆杞€佽兘閲忔弿绾裤€佽В閿?
- Deadline: `2026-10-29`
- Delivery goal: 绉佸瘑銆佺ǔ瀹氥€佹墜鏈哄彲鐢ㄧ殑鍛ㄥ勾绾康绀肩墿銆?- Base: V1 `blocks + build.py + site/index.html`銆?- Runtime config version: `1.8.3`銆?
## Current Architecture

Frontend: GitHub Pages 闈欐€侀〉闈€?
Backend: Supabase Lite / Anniversary Bridge锛?- Auth: Email + Password
- Database: `books`, `book_members`, `book_data`
- Storage: private bucket `starbook-media`
- Realtime: **not enabled for anniversary release**
- PWA: **not enabled for anniversary release**

## Runtime Context

- `SB.user`: 褰撳墠鐧诲綍鐢ㄦ埛 / Session銆?- `SB.book`: 褰撳墠鏁版嵁 Book 涓庣敤鎴疯鑹诧紙Supabase Runtime Context锛夈€?- `SB.magicBook`: Magic Celestial 灏侀潰涓庡紑涔﹀姩鐢绘帶鍒跺櫒锛涗笉寰椾笌 `SB.book` 鍚堝苟銆?- `SB.theme.current`: 褰撳墠 `magic-celestial`銆?- `SB.experience.current`: 褰撳墠 `world-map`銆?- `SB.store`: V1 鍏煎鏁版嵁鎺ュ彛锛屽唴閮ㄨ鍙?`book_data.payload`銆?
Current Book:
- id: `8a3cc6fe-b667-4ce7-b47b-79cebc0e1353`
- name: `鏄熷笨涔嬩功`
- relationship: `romantic`
- theme: `magic-celestial`
- experience: `world-map`

## Anniversary Bridge Data

`book_data.payload` 褰撳墠缁х画淇濆瓨 V1锛?
```json
{
  "cities": {},
  "memories": {},
  "settings": {}
}
```

杩欐槸涓存椂鍏煎灞傦紝涓嶆槸鏈€缁?V2 鏁版嵁妯″瀷銆?
`revision` 鐢ㄤ簬杞婚噺骞跺彂鍐茬獊妫€娴嬨€?
## Storage Convention

Private bucket: `starbook-media`

```text
{book_id}/images/{generated-id}.jpg
{book_id}/audio/{generated-id}.mp3|m4a|...
```

濯掍綋灞炰簬 Book锛屼笉灞炰簬鍗曚釜 User銆?
## Architecture Invariants

1. Starbook 蹇呴』淇濈暀澶氱敤鎴锋墿灞曡兘鍔涖€?2. 涓€涓敤鎴锋湭鏉ュ彲浠ユ嫢鏈夋垨鍔犲叆澶氭湰 Book銆?3. 涓€鏈?Book 鍙互鏈夊涓垚鍛樸€?4. 涓嶅厑璁镐笟鍔′唬鐮佸亣璁剧郴缁熸案杩滃彧鏈変竴鏈?Book銆?5. 涓嶅厑璁?Starbook Core 鍋囪鎵€鏈?Book 閮芥槸鎯呬荆鍏崇郴銆?6. Relationship Type 涓?Theme 鐙珛銆?7. Theme 涓?Experience 鐙珛銆?8. `magic-celestial` 鍙槸绗竴濂?Theme銆?9. `world-map` 鍙槸绗竴濂?Experience銆?10. Memory 鏈潵涓嶅緱寮哄埗瑕佹眰 Location / City銆?11. Book 鍐呬笟鍔℃暟鎹繀椤绘湁鏄庣‘ Book 鎵€灞炲叧绯汇€?12. 褰撳墠鏈紑鏀剧殑鏈潵鑳藉姏浼樺厛閫氳繃閰嶇疆鍏抽棴锛岃€屼笉鏄牬鍧忔墿灞曟帴鍙ｃ€?13. 2026-10-29 鍓嶏紝鍛ㄥ勾鐗堢ǔ瀹氭€ч珮浜庢灦鏋勭函娲佸害鍜屽姛鑳芥暟閲忋€?14. 涓嶄负鍛ㄥ勾鐗堝紩鍏?React / Vue / Vite 澶ц縼绉汇€?15. 涓嶅湪娴忚鍣ㄦ垨浠撳簱涓斁 Supabase Secret / service_role / 鏁版嵁搴撳瘑鐮併€?
## Project Governance / Agent Handoff

浠?v1.5.1 璧凤紝椤圭洰涓婁笅鏂囦笌绠＄悊閾捐矾姝ｅ紡鍥哄寲鍦ㄤ粨搴撳唴锛?
- `AGENTS.md`: 鏂?Agent 蹇呰鍏ュ彛銆?- `docs/PROJECT_MANAGEMENT_FULL_CHAIN.md`: 寮€鍙?鈫?鏍￠獙 鈫?PR 鈫?main 鈫?Pages 鈫?鏁版嵁淇濈暀 鈫?鍥炴粴鍏ㄩ摼璺€?- `docs/ARCHITECTURE_EXTENSION_CONTRACT.md`: 澶氱敤鎴?/ 澶?Book / Relationship / Theme / Experience 闀挎湡鎵╁睍濂戠害銆?- `docs/DATA_LIFECYCLE.md`: Supabase 鏁版嵁鐢熷懡鍛ㄦ湡涓?migration 瑙勫垯銆?- `docs/RELEASE_WORKFLOW.md`: 鐗堟湰鍙戝竷鎿嶄綔璇存槑銆?- `docs/releases/vX.X.X.md`: 姣忕増鏈繀椤昏褰?Runtime銆佹暟鎹€丆I銆侀儴缃插拰娌荤悊閾捐矾鍙樺寲銆?
Production governance:

```text
release/vX.X.X or feature/*
鈫?Pull Request
鈫?validate-starbook
鈫?merge main
鈫?Deploy Starbook to GitHub Pages
```

`main` 鏄敮涓€ Production branch銆傛櫘閫氫唬鐮佸彂甯冧笉閲嶇疆 Supabase 鏁版嵁銆?

## Book Opening (v1.8.3)

- 寮€涔?= 鏈哄叧鍚皝锛坄SB.magicBook.awaken(on)` / `unlock()`锛?.9s锛夆啋 鍚皝锛坄fxOpen`锛屾墘椤甸噾澧ㄦ槦鍥?+ 鏄熷皹锛夆啋 鍏ラ〉 鈫?闂ㄩ挜鍖欍€傝瑙?`prompts/04-book-opening.md`銆?- 鍙敤 transform / opacity / 鐭椂鎻忕嚎锛涘皬榻胯疆 SVG 鑷浆鍙湪鏈哄叧鍚姩鐨?2 绉掑唴瀵规墍鏈夋。浣嶅紑鍚€?
## Mobile Performance (v1.8.2)

- 寮€涔︽湡闂寸姝㈠垱寤?WebGL锛堜笉璋冪敤 `SB.scenes.prefetch('globe')`锛夛紱鍦扮悆鍦ㄩ棬閽ュ寵鐩栨弧鍚庡噯澶囥€?- 榄旀硶涔︾鏂囩幆鏄?2D 鎶曞奖鐨勫墠 / 鍚庝袱灞傦紙`#bk-runes-front` / `#bk-runes-back`锛夛紝涓嶅緱鏀惧洖 3D `preserve-3d` 涓婁笅鏂囷紙鎵嬫満 WebKit 浼氬垏鍓茬浉浜ゅ钩闈㈠鑷撮棯鐑侊級銆?- 鏌斿拰妗ｏ紙鎵嬫満榛樿锛夊叧闂槀璐电殑娣峰悎妯″紡 / 閬僵灞傚苟浣跨敤寤変环鐑噾婊ら暅锛涜杽鐑熷彧鍦ㄥ崕涓芥。銆佹甯告贩鍚堛€?- 鐨潻 / 绾稿紶绾圭悊缂撳瓨鍦?localStorage锛涙斁鏄犲櫒绾圭悊寤惰繜鐢熸垚銆?- 鍙充笂瑙掓爣璇嗙粍鏂板銆屽洖鍒伴瓟娉曚功銆嶏紙`SB.dock` 鐨?action 绫绘爣璇嗭級銆?
## Visual / Layout (v1.8.1)

- 杞満鎸夎矾绾垮尯鍒嗭紙`SB.gate.kinds = portkey / nox / quill / pensieve` + `portal` 瑁呴グ锛夛細`flash`=闂ㄩ挜鍖欙紙涔?/ 鑿滃崟 鈫?鍦扮悆锛夈€乣portal`=骞诲奖鏄惧舰锛堝湴鐞?鈫?鍥藉锛夈€乣quill`=澧ㄩ噾涔﹂〉锛堚啋 鍩庡競銆佲啋 鏃跺厜闀垮嵎锛夈€乣pensieve`=鍐ユ兂鐩嗭紙鈫?鏀炬槧锛夈€乣veil`=鐔勭伅鍣紙杩斿洖锛夈€傛洕鍏夎鍒欒 `prompts/00-gate.md`銆?- 榄旀硶涔︽潗璐ㄣ€屾槦澶滄懇娲涘摜鐨€嶏細鍗堝闈涜摑鐨潻銆侀妲熷彜閲戙€佺洸鍘嬭姳杈广€侀暥宓屾槦杈般€佸彜閲戝寘瑙掞紙`blocks/03-magic-book.html`锛夈€?- 鑿滃崟鍙湁銆屼笘鐣屾槦鍥俱€嶃€屾椂鍏夐暱鍗枫€嶏紱闊充箰 / 鍔ㄦ晥 / 璐︽埛鍦ㄥ彸涓婅 `SB.dock`锛坄blocks/02y-dock.html`锛屽悇鍧楃敤 `SB.dock.add` 娉ㄥ唽闈㈡澘锛夈€傚叏绔欒儗鏅煶涔愮鐞嗗湪闊充箰闈㈡澘閲屻€?- 銆屾椂鍏夐暱鍗枫€嶏紙鍦烘櫙 id 浠嶄负 `overview`锛夛細妯悜鍙嫋鍔ㄦ椂闂磋酱锛涙斁鏄犲弬鏁?`from:'overview'` 鏃惰繑鍥炲埌鏃跺厜闀垮嵎銆?- 鍩庡競绌虹姸鎬侊細涓庣珷鑺傚崱鐗囧悓姣斾緥鐨勭┖鐧界珷鑺傚崱銆?
## Visual / Navigation (v1.8.0)

- 鍦烘櫙娴佺▼锛氶瓟娉曚功 鈫?涓栫晫鏄熷浘锛堝湴鐞?+ 鎼滅储鏍忥級鈫?鍥藉鍦板浘 鈫?鍩庡競鐩綍 鈫?鍥炲繂鏀炬槧銆?*澶ф床鍥藉鐩綍椤靛凡鍒犻櫎**锛涘浗瀹剁殑鐖剁骇鏄?`globe`锛岃繑鍥炴椂鍦扮悆鑷姩杞悜璇ュ浗瀹躲€?- 杞満 `SB.gate`锛坄blocks/01b-gate.html`锛夛細`flash` = 闂ㄩ挜鍖欍€乣portal` = 骞诲奖鏄惧舰瑁呴グ銆乣veil` = 鐔勭伅鍣?/ 鑽у厜闂儊锛涘彧鏇挎崲 cover / reveal 瑙嗚锛孲cene Runtime 浜嬪姟涓嶅彉锛涚己澶辨椂鍥為€€鏃ц瑙夛紝寮傚父 `abort()`銆?- 鎼滅储锛歚SB.WORLD_CITIES`锛?48 鍩庣绾垮簱锛宍tools/make_cities.py` 鐢熸垚锛? Open-Meteo Geocoding 鍦ㄧ嚎鎼滅储锛堝敮涓€鏂板澶栭儴鏈嶅姟锛屽け璐ラ檷绾э級锛沗SB.globe.focus(o)` / `SB.globe.search(q)` 渚涜皟璇曘€?- 榄旀硶涔︺€屾槦杈夊眰娆°€嶏細鏄熶簯銆佸疂鐭冲厜婧?/ 鍏夋潫銆?D 绗︽枃鐜€佺儫闆剧伀鏄熺敾甯冦€佷功椤佃竟缂樻祦鍏夛紱`SB.magicBook.fxSuck(on)` 鐢ㄤ簬寮€涔﹀惛鍏ャ€?- 鍦扮悆銆屾槦杈夊眰娆°€嶏細娴烽潰楂樺厜銆佷簯闆惧眰銆佸灞傚厜鏅曘€佹槦搴х嚎銆佹槦鐩樼幆銆佽冻杩瑰厜寮с€?- 鎻愮ず璇嶏細`prompts/00-gate.md`銆乣prompts/03-magic-book.md`銆乣prompts/07-globe.md`銆乣prompts/09-country-map.md`锛涜皟鐮旓細`docs/design/VISUAL_UPGRADE_PLAN.md` 绗?8 鑺傘€?
## Scene Runtime / Performance Baseline (v1.7.3)

- Scene 鐢熷懡鍛ㄦ湡锛歚prepare 鈫?cover 鈫?await enter 鈫?nextPaint 鈫?reveal 鈫?cleanup`銆?- `SB.scenes.prefetch(id, params)` 鍙鐑紝涓嶆敼鍙樺綋鍓嶅満鏅€?- 鐧诲綍 Gate 蹇呴』绛?`SB.store.ready + scenes.boot(book) + first paint` 鍚庡啀鎻紑銆?- Store 鍚姩鍙鍙?JSONB锛屼笉鍏ㄩ噺绛炬暣鏈功濯掍綋 URL銆?- Globe / Country / City / Player 閮藉簲鍦ㄦ彮绀哄墠鍑嗗棣栧睆鍏抽敭璧勬簮銆?- 瀵瑰簲閫愰摼璺?Prompt 浣嶄簬 `prompts/performance/`銆?
## Visual / Typography (v1.5.2)

- 涓枃鍏ㄧ珯缁熶竴 Noto Serif SC锛堟€濇簮瀹嬩綋锛夛紱鎷変竵閾枃 Cinzel锛涙暟瀛?Cormorant Garamond锛涘潎鏉ヨ嚜 Google Fonts銆?- ZCOOL XiaoWei 涓?Cinzel Decorative 宸茬Щ闄わ紙瀛楀舰鎹熷潖 / 鏁板瓧闅捐鲸锛夛紝`tools/check_project.py` 闃插洖褰掋€?- 鍥炬爣缁熶竴鐢?`SB.icon(name)` 鍐呰仈 SVG锛屼笉渚濊禆绯荤粺绗﹀彿瀛椾綋銆?- 瑙嗚鍗囩骇鍚庣画鐗堟湰璁″垝锛歚docs/design/VISUAL_UPGRADE_PLAN.md`锛坴1.6.0 鐢靛奖寮忔斁鏄犮€乿1.6.1 杞満銆乿1.6.2 榄旀硶涔?鍦扮悆鐗规晥锛夈€?
## Visual / Cinematic Player (v1.6.0)

- 鍥炲繂鏀炬槧 = 鏀炬槧鍘咃紙娴锋姤 + 鏀炬槧鎸夐挳锛夆啋 寮€鍦猴紙鐔勭伅銆侀摱骞曢粦杈广€佸ⅷ婊存稛婕€佹墘椤碉級鈫?闀滃ご锛堟帹/鎷?妯憞/绾垫憞/鎮诞鐩哥墖锛屾憾瑙?/ 鍏夋紡 / 澧ㄦ淮鎻箷杞満锛岀數褰卞瓧骞曪級鈫?缁堢珷锛堥棯鐧姐€併€岀粓 路 FINIS銆嶃€佸啀鏀句竴閬嶏級銆?- 鐢卞崟涓€鏃堕挓椹卞姩锛屾殏鍋滃嵆鍐荤粨锛涘彧璇荤幇鏈?memory 瀛楁锛坱itle / date / note / cover / slides / bgm / bgmMode锛夛紝鏃犳暟鎹彉鍖栥€?- 鐩稿唽鍗＄墖鍙充笅瑙掋€屾斁鏄犮€嶆寜閽洿鎺ュ紑濮嬫斁鏄狅紱鐐瑰崱鐗囧叾浠栦綅缃繘鍏ユ斁鏄犲巺銆?- `SB.audio.duck(level, ms)`锛氱粓绔犻煶涔愭笎寮卞埌 30%锛沗SB.player`锛氳皟璇?娴嬭瘯鐢ㄧ殑 play / seek / jump / state銆?- 鎻愮ず璇嶏細`prompts/11-memory-player.md`锛涜皟鐮旓細`docs/design/VISUAL_UPGRADE_PLAN.md` 绗?6 鑺傘€?
## Visual / Multi-photo Player 路 Styles 路 Seasons (v1.7.0)

- 鏀炬槧鐢便€屽婕斻€嶇紪鎺掓垚澹版槑寮忔椂闂寸嚎锛堢収鐗?/ 鏂囧瓧 / 杩炵嚎 / 鍏夋紡鍏冪礌 + 鍏抽敭甯э級锛屾覆鏌撳櫒鍙寜鏃堕挓 T 璁＄畻 鈫?鍙殏鍋溿€佸彲 seek锛涚敾闈㈤噷甯告湁 2鈥? 寮犵収鐗囨帴鍔涙洿鏇裤€?- 涓夌鏀炬槧椋庢牸锛歚cinema` 閾跺箷锛堥粯璁わ細鍏ㄥ箙 + 鍙岃仈 / 涓夎仈鍒嗗睆銆佸厜缂?/ 铏硅啘 / 鐧惧彾 / 鎿﹀叆 / 鎵╁睍 / 寮€闂ㄨ浆鍦恒€佺珫鎺掑ぇ瀛楀箷锛夈€乣constellation` 鏄熷浘锛堟槦绌轰腑鐑噾鐩告鎺ュ姏 + 鏄熷骇杩炵嚎 + 缂栬緫寮忕紪鍙峰瓧骞曪級銆乣journal` 鎵嬫湱锛堢儧鍏変功妗屻€佺浉鐗囪惤涓嬪爢鍙犮€侀暅澶磋窡闅忋€佸ⅷ杩规墜鍐欐梺鐧斤級銆?- 鍥涘涓婚锛氭槬妯?/ 澶忓厜钀?/ 绉嬫灚 / 鍐洩 + 璋冭壊锛涙斁鏄犲巺涓庢斁鏄犳帶鍒舵潯鍙复鏃跺垏鎹€?- 鍥炲繂鏂板**鍙€?*瀛楁 `style`銆乣season`锛圱heme 琛ㄧ幇鍋忓ソ锛岀己鐪?= `cinema` / `auto`锛夛紝鏃?migration銆佷笉鏀?schema_version銆?- 鍥炲繂缂栬緫鍣ㄥ崌绾т负銆屾槦灞挎墜绋裤€嶏細瀹炴椂娴锋姤棰勮 + 鏁呬簨 / 褰卞儚 / 鏀炬槧 / 涔愮珷鍥涚珷銆?- `SB.cinema`锛氶鏍?/ 瀛ｈ妭鍏叡瀹氫箟锛沗SB.player` 鏂板 `setStyle / setSeason / estimate`銆?- 鎻愮ず璇嶏細`prompts/11-memory-player.md`銆乣prompts/12-memory-editor.md`锛涜皟鐮旓細`docs/design/VISUAL_UPGRADE_PLAN.md` 绗?7 鑺傘€?
## Visual / City Album (v1.7.1)

- 鍩庡競鍥炲繂鐩綍锛堝潡 10锛夋敼涓哄崟鍒楅噾鑹叉椂闂寸嚎 + 绔犺妭鍗＄墖锛氱綏椹暟瀛楃珷鑺傚窘璁般€佺儷閲戞捣鎶ワ紙椋庢牸 / 瀛ｈ妭寰界珷涓庡鑺傝皟鑹诧級銆佹爣棰樸€佺収鐗囨暟涓庨璁℃斁鏄犳椂闀裤€佷竴娈佃瘽鎽樺綍銆佺収鐗囩缉褰辨潯锛屽崱鐗囦笂鐩存帴銆屾斁鏄?/ 鏀炬槧鍘?/ 缂栬緫銆嶃€?- 椤电湁锛氱紦鎱㈡棆杞殑娉曢樀銆佸煄甯傚悕銆佺粺璁¤兌鍥婏紙鍥炲繂鏁?/ 鐓х墖鏁?/ 鏃堕棿璺ㄥ害锛夈€併€屾柊鐨勫洖蹇嗐€嶆寜閽紱鏃堕棿绾挎湯灏俱€屽啓涓嬬 N 绔犮€嶏紱绌虹姸鎬佹敼涓烘繁鑹茬儷閲戙€岀┖鐧界珷鑺傘€嶃€?- 鍙鐜版湁瀛楁锛屾棤鏁版嵁鍙樺寲锛涙彁绀鸿瘝 `prompts/10-city-album.md`锛岃皟鐮?`docs/design/VISUAL_UPGRADE_PLAN.md` 7.6 鑺傘€?
## Performance / Responsive Baseline (v1.7.2)

- 鍦烘櫙鍒囨崲锛歚portal` 涓嶅啀鎶婃棫鍦烘櫙淇濇寔 active 鍒板姩鐢荤粨鏉燂紱veil / flash / portal 鎸夎澶囨€ц兘缂╃煭鏃堕暱锛屽苟鍦?scene swap 鍚庣瓑寰呮祻瑙堝櫒瀹屾垚 paint锛屽噺灏戞畫褰变笌鍗″抚銆?- 鎬ц兘妗ｏ細缁煎悎 viewport銆乧oarse pointer銆丆PU core銆乨evice memory 鍒ゅ畾 `high / low / reduced`锛沴ow 妗ｉ檷浣庡叏灞€绮掑瓙鏁伴噺銆丆anvas DPR 涓庡姩鐢诲埛鏂扮巼銆?- 鏀炬槧锛氭挱鏀惧櫒 low / mobile 妗ｇ害 30 FPS锛涙挱鏀炬湡闂?Ambient FX 鑷姩闄嶅抚锛涜繘鍏ユ斁鏄犲巺鍓嶉鐑?Signed URL 涓庡墠鍑犲紶鐓х墖锛屾挱鏀句腑棰勫彇 12鈥?6 绉掔獥鍙ｃ€?- 鍩庡競鐩綍锛氶灞忓皝闈紭鍏堬紝鍏朵粬娴锋姤 / 缂╁奖 lazy锛涙墜鏈哄噺灏戠缉褰卞苟鍚敤 `content-visibility:auto`锛岄檷浣庨暱鍒楄〃甯冨眬銆佸浘鐗囦笅杞戒笌瑙ｇ爜鍘嬪姏銆?- 缂栬緫鍣細鐓х墖缃戞牸 lazy decode锛涙闈?/ 鎵嬫満閲嶆柊绾︽潫缂栬緫鍣ㄥ搴︺€佹捣鎶ヤ笌鐓х墖鍗＄墖姣斾緥锛涚獎灞忕収鐗囧崱鐗囨敼涓哄崟鍒楋紝閬垮厤鍙紪杈戝尯鍩熻繃灏忋€?- 鏂颁笂浼?Private Storage 濯掍綋浣跨敤鍞竴鏂囦欢鍚?+ 闀跨紦瀛樺厓鏁版嵁锛涗笉浼氫慨鏀规棫瀵硅薄鎴栫幇鏈夋暟鎹€?- 鎬ц兘绾︽潫鏂囨。锛歚docs/PERFORMANCE_GUIDE.md`銆?
## Known Technical Debt

- `book_data.payload` 鏄暣浣?JSONB锛屽悗缁渶瑕佹瑙勫寲銆?- Memory 褰撳墠浠嶄笌 City 寮鸿€﹀悎銆?- Theme / Experience 鐩墠鍙湁 Context锛屾病鏈夋彃浠跺姞杞藉櫒銆?- Signed URL 浠呭仛鍐呭瓨缂撳瓨锛涘埛鏂板悗閲嶆柊绛惧悕銆?- 鏍稿績 Third-party CDN 灏氭湭鍏ㄩ儴鏈湴鍖栵紙Google Fonts 浠嶄负澶栭儴渚濊禆锛涘姞杞藉け璐ユ椂鍥為€€绯荤粺瀹嬩綋锛岀増寮忎笉鍙橈級銆?- 瀹屾暣娣卞眰 URL Router 灏氭湭瀹炵幇銆?- 鏆傛湭浣跨敤 Realtime銆?- 鍥剧墖浠嶆槸鍗曚竴鍘嬬缉灏哄銆?
## Live Supabase Status

Confirmed by owner on 2026-10-26:
- `001_anniversary_bridge.sql`: executed successfully.
- `002_anniversary_owner.sql`: executed successfully.
- Book seed query returned one row.
- `starbook-media`: confirmed `public = false`.

v1.5.1 planned forward migration:
- `002_v151_title_and_members.sql`: run after the v1.5.1 code release (or before final verification).
- Updates Book display name to `鏄熷笨涔嬩功`.
- Adds active editor `11aa32fe-3875-4880-81fb-02a543dca853`.
- Adds active editor `62adee54-c59a-4844-abb5-1b5629da3bf9`.
- Does **not** modify `book_data.payload` or Storage.

## Core live interaction verification

Confirmed by owner on 2026-10-26:
- Production URL can open successfully.
- Auth login / auth recovery paths work.
- Magic Book scene opens correctly.
- Globe drag and continent/country interactions work.
- Current mobile / back-navigation stability test has no observed blocker.

## Phase 2 interaction hotfix

- 宸蹭慨澶?`SB.book` 鍛藉悕鍐茬獊锛歏1 榄旀硶涔﹀姩鐢绘帶鍒跺櫒宸查噸鍛藉悕涓?`SB.magicBook`銆?- 鍘熷洜锛歊untime 澶?Book Context 涓?V1 瑙嗚鎺у埗鍣ㄦ浘瑕嗙洊鍚屼竴鍏ㄥ眬鍛藉悕绌洪棿锛屽彲鑳藉鑷?Store 鍙栦笉鍒板綋鍓?Book 骞堕€犳垚鐧诲綍鍚庝氦浜掑紓甯搞€?- 淇鍚庡繀椤婚噸鏂伴獙璇侊細鐧诲綍 鈫?榄旀硶涔?鈫?鍦扮悆鎷栨嫿 鈫?澶ф床 鈫?鍥藉銆?
## Auth / Access Recovery Hotfix

- 瀵嗙爜鎴栧嚟鎹敊璇細淇濈暀鍦ㄧ櫥褰曡〃鍗曪紝鍏佽绔嬪嵆淇敼鍚庨噸璇曘€?- 宸茶璇佷絾娌℃湁褰撳墠 Book Membership锛氭彁渚涒€滈噸鏂版鏌ユ潈闄愨€濆拰鈥滆繑鍥炵櫥褰曗€濄€?- RLS / 鏉冮檺 / Database 寮傚父锛氭彁渚涒€滈噸鏂板皾璇曗€濆拰鈥滆繑鍥炵櫥褰曗€濓紝閬垮厤閿欒椤甸攣姝荤敤鎴枫€?- 鈥滆繑鍥炵櫥褰曗€濅細 sign out 褰撳墠 Supabase Session锛屽苟娓呯┖ `SB.book` Runtime Context銆?
## Phase 3 Stability Hardening

- 鍏ㄥ眬瑙嗗彛浼樺厛浣跨敤 `100dvh`锛屼繚鐣?`100vh` fallback銆?- coarse pointer 涓嬮€氱敤鎸夐挳銆佸鑸拰鑿滃崟鎵╁ぇ瑙︽帶鐩爣銆?- `SB.loadScript()` 澧炲姞鍗曟簮瓒呮椂涓庤嚜鍔?fallback銆?- Three.js 褰撳墠淇濈暀涓?CDN fallback锛涙湰鍦?vendor 鍖栦粛鏄悗缁彲閫変紭鍖栵紝涓嶉樆濉炲懆骞翠氦浠樸€?- 鍦烘櫙鍘嗗彶鍔犲叆 `_pendingHistory`锛岃繛缁?Android / 娴忚鍣ㄨ繑鍥炴椂浠ユ渶鍚庝竴娆?history state 涓哄噯銆?- bfcache 鎭㈠浼氭竻鐞嗗彲鑳芥畫鐣欑殑 busy / veil / flash銆?- Globe / Country Map 鍦ㄨЕ鎺ц澶囦笂浣跨敤鏇村鏉剧殑鎷栧姩闃堝€硷紝鍑忓皯璇Е銆?
## Highest Priority Next

1. 鍙戝竷 v1.8.3锛坄.\release-current.ps1`锛夛紝鐢?iPhone 瀹炴祴寮€涔︺€屾満鍏冲惎灏併€嶏細榻胯疆閫愮骇鍜斿搾杞姩銆佸疂鐭虫棆杞€佺儷閲戞弿浜€佽В閿侊紝鍐嶆帴鏄熷浘涓庡厜闂紱鍚屾椂纭娌℃湁鍗￠】涓庤繃鏇濄€?2. 瀹屾垚 Private Storage 姝ｅ紡鐓х墖涓?BGM 鐨勫疄闄呭唴瀹瑰～鍏咃紝骞朵紭鍏堜娇鐢?v1.7.2 涔嬪悗鐨勬柊涓婁紶缂撳瓨绛栫暐銆?3. 鏍稿績绋冲畾鍚庡疄鐜板懆骞存墘椤?/ 鐚瘝 / 缁撳熬锛圓NN-008锛夈€?4. 杩涜鏈€缁堟墜鏈虹 Production URL 楠屾敹锛涢噸鐐硅瀵熷急缃戠収鐗囩瓑寰呫€佸彂鐑€佹帀甯т笌椤甸潰娈嬪奖銆?5. 2026-10-28 鏅?Feature Freeze锛泇1.8.0 涔嬪悗鍙慨 bug銆傝嫢鐪熸満涓婃柊杞満鍗￠】锛屽彲鍦ㄨ彍鍗曘€屽姩鏁堝己搴︺€嶉€夋嫨鏌斿拰 / 鍏抽棴锛坮educed 妗ｄ笉鏄剧ず闂級銆?
## Release Automation (v1.6.0+)

鐗堟湰瀹屾垚鍚庣殑棣栭€夊叆鍙ｏ細

```powershell
.\release-current.ps1
```

璇ヨ剼鏈互 `VERSION` 涓哄敮涓€鐩爣鐗堟湰鏉ユ簮锛岃嚜鍔ㄨ鑼?`release/vX.X.X`銆佽ˉ榻愮己澶?Release Record銆佺敓鎴?`scripts/releases/release-vX.X.X.ps1`銆佸悓姝ョ粨鏋勫寲鐗堟湰澹版槑锛屽苟璋冪敤 `publish.ps1` 杩涘叆 PR / validate / main / Pages銆?
鍙戝竷鑷姩鍖栦笉浼氭墽琛?Supabase SQL锛屼笉浼?reset Database / Storage锛沵igration 浠嶆槸鏄庣‘鐨勪汉宸?Production 鎿嶄綔銆?