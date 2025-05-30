import os

def convert_to_utf8(directory):
    for root, _, files in os.walk(directory):
        for file in files:
            if file.endswith(".py"):
                filepath = os.path.join(root, file)
                try:
                    # CP949 혹은 EUC-KR로 시도
                    with open(filepath, "r", encoding="cp949") as f:
                        content = f.read()
                    # UTF-8로 덮어쓰기
                    with open(filepath, "w", encoding="utf-8") as f:
                        f.write(content)
                    print(f"✅ 변환됨: {filepath}")
                except UnicodeDecodeError:
                    print(f"⚠️ 건너뜀 (변환 불가): {filepath}")
                except Exception as e:
                    print(f"❌ 에러 발생 ({filepath}): {e}")

if __name__ == "__main__":
    convert_to_utf8(".")
