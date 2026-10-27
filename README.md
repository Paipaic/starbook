# 鏄熷笨涔嬩功 Starbook

褰撳墠姝ｅ紡椤圭洰鐗堟湰锛?*v1.8.0**銆?
杩欐槸涓€涓互娌夋蹈寮忊€滆蹇嗕功鈥濅负鏍稿績鐨勭浜烘暟瀛楄蹇嗛」鐩€傚綋鍓嶇敓浜у舰鎬佹槸 `romantic + magic-celestial + world-map`锛屼絾搴曞眰鏋舵瀯宸茬粡涓哄鐢ㄦ埛銆佸 Book銆佸鍏崇郴绫诲瀷銆佸 Theme銆佸 Experience 鐨勫悗缁墿灞曚繚鐣欒竟鐣屻€?
## 鏂?Agent / 鏂板紑鍙戠獥鍙?
**涓嶈鐩存帴浠庝唬鐮佸紑濮嬨€?*

绗竴姝ヨ闃呰锛歔`AGENTS.md`](AGENTS.md)

闅忓悗涓ユ牸鎸夌収鍏朵腑瀹氫箟鐨勯『搴忚鍙?`PROJECT_STATE.md`銆佸叏閾捐矾绠＄悊鏂囨。銆佹墿灞曞绾︺€佹暟鎹敓鍛藉懆鏈熴€丆HANGELOG銆丷OADMAP 鍜屽綋鍓?Release Record銆?
## Production

```text
release/* or feature/*
鈫?Pull Request
鈫?validate-starbook
鈫?main
鈫?GitHub Actions
鈫?GitHub Pages
```

`main` 鏄敮涓€ Production branch銆係upabase Database / Private Storage 涓?Git 鍒嗘敮鐢熷懡鍛ㄦ湡鐙珛锛屾櫘閫氫唬鐮佺増鏈彂甯冧笉浼氶噸缃湡瀹炲洖蹇嗘暟鎹€?
## 褰撳墠 Book

- 鍚嶇О锛?*鏄熷笨涔嬩功**
- Relationship锛歚romantic`
- Theme锛歚magic-celestial`
- Experience锛歚world-map`

## 鍙戝竷鍓?
```powershell
python build.py
python tools/check_project.py
```

姝ｅ紡鐗堟湰蹇呴』鍚屾缁存姢 `VERSION`銆乣CHANGELOG.md`銆乣ROADMAP.md`銆乣PROJECT_STATE.md` 涓?`docs/releases/vX.X.X.md`銆?
## 涓€閿彂甯?
浠?v1.6.0 璧凤紝瀹屾垚鏂扮増鏈凯浠ｅ悗浼樺厛浣跨敤锛?
```powershell
.\release-current.ps1
```

鑴氭湰浠?`VERSION` 鑷姩璇嗗埆鐗堟湰锛岃嚜鍔ㄨˉ榻愮己澶?Release Record銆佺敓鎴?`scripts/releases/release-vX.X.X.ps1`锛屽啀鎵ц build / validation / PR / Auto-merge銆傝缁嗚鏄庤 [`docs/RELEASE_AUTOMATION.md`](docs/RELEASE_AUTOMATION.md)銆?