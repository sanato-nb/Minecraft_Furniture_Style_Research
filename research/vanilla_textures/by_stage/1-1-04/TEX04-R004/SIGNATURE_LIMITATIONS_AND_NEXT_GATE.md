# TEX04-R004 — SHA-384 매니페스트 체인 검증의 의미 및 공식 인증 게이트

## 검사된 것

- 사용자 업로드 `1.21.11/`의 실제 PNG 9개/정적 JSON 21개의 내용이, 함께 업로드된 `META-INF/MANIFEST.MF`의 대응 `SHA-384-Digest`와 모두 일치.
- 해당 매니페스트 30개 항목을 **CRLF 줄바꿈으로 재구성했을 때**, 각각의 SHA-384가 함께 업로드된 `MOJANGCS.SF` 항목과 모두 일치.
- `MOJANGCS.SF`의 `SHA-384-Digest-Manifest-Main-Attributes`와 매니페스트의 주요 속성 섹션 SHA-384도 일치.
- 서명 관련 `MOJANGCS.RSA` 파일 존재를 GitHub 메타데이터로 확인했으나 **내용의 암호학적 검증은 수행하지 않음**.

## 검사되지 않은 것

- `MOJANGCS.RSA`의 PKCS#7 SignedData 유효성, 서명된 SF 전체 바이트, 발급자 인증서/신뢰체인의 유효성 (미검증).
- GitHub에 저장된 줄바꿈 LF 자료가 원래 JAR 내의 정확한 CRLF 바이트와 동일한지에 대한 원본 ZIP 엔트리 대조 (미검증).
- Mojang HTTPS 버전 매니페스트와 버전 JSON 원본을 직접 가져와 SHA1·size 체인으로 인증하는 절차 (미완료).
- 배포 `client.jar` 전체 바이너리를 해시하여 Mojang `downloads.client.sha1`/size에 대조하는 절차 (미완료).
- 실제 Minecraft 인게임 1.21.11 정적 장면을 통제된 환경에서 관찰·캡처하는 절차 (미완료).

따라서 **파일 내용→업로드된 매니페스트→업로드된 .SF의 항목별 해시 일치**는 확인했지만, 이 결과만으로 **Mojang 배포 원본 인증** 또는 **실제 게임 렌더 검증**이라고 선언해서는 안 된다.

## 재현

`python VERIFY_SIGNED_MANIFEST_CHAIN.py /path/to/1.21.11 --out /path/to/results`

사용자의 정확한 PNG 9개/JSON 21개가 포함된 디렉터리를 전달하면 두 텍스트에서 해시/줄바꿈 구조를 읽어 총 30건과 주요 속성의 SHA-384를 재계산한다. **오프라인 재현 스크립트는 JAR 전체 SHA1·RSA 전자서명·인게임 검증을 수행하지 않는다.**
