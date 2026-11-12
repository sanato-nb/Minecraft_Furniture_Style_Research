# GitHub 업로드 방법

## 1. 새 저장소 생성

- Owner: `sanato-nb`
- Repository name: `Minecraft_Furniture_Style_Research`
- Description: `Minecraft vanilla texture, 3D model, UV, blockstate and furniture-style research (Java 1.21.11).`
- Visibility: **Private 권장** (공개 검토 후 Public 가능)
- Add README: **Off** (이미 README.md 포함됨)
- Add .gitignore: **No .gitignore** (이미 포함됨)
- Add license: **No license** (권리·배포 조건 검토 전)

## 2-A. 웹 화면을 통한 업로드

1. 패키지 ZIP 압축을 풉니다.
2. GitHub 저장소 페이지의 **uploading an existing file** 링크 또는 **Add file → Upload files**로 들어갑니다.
3. 압축을 푼 `Minecraft_Furniture_Style_Research` 폴더 안의 파일과 하위 폴더를 드래그해 업로드합니다(Chrome에서 폴더 드래그 지원). **ZIP 파일 하나만 올리면 GitHub에서 내부 내용을 탐색할 수 없으므로 압축을 풀어 올려야 합니다.**
4. **Commit changes**를 누릅니다.
5. `README.md`, `PROGRESS.md`, `data/MC_Furniture_Style_Stage1_Research_v8.sqlite`가 정상 업로드됐는지 확인합니다.

## 2-B. Git 명령으로 업로드 (Git 설치 필요)

Git Bash 또는 PowerShell에서 압축을 푼 폴더로 이동한 후 실행:

```powershell
cd "Minecraft_Furniture_Style_Research"
git init
git branch -M main
git add .
git commit -m "Add Minecraft furniture style research checkpoints v1-v8"
git remote add origin https://github.com/sanato-nb/Minecraft_Furniture_Style_Research.git
git push -u origin main
```

저장소가 이미 README 초기화 커밋으로 생성된 경우에는 위 명령으로 바로 푸시하면 충돌할 수 있습니다. 그런 경우 **빈 저장소를 만들거나 clone → 파일 복사 → commit → push**하는 절차를 사용하세요.

## 3. 학습 연속성 확인

다른 ChatGPT 대화에 저장소 URL을 공유하고 **README + PROGRESS + 최신 SQLite DB**를 기준으로 이어가면 됩니다. GitHub 저장소는 기억 자체가 아니라 *외부에 저장한 연구 결과*입니다.
