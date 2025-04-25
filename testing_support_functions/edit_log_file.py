import os
import glob

def rename_latest_file(folder_path, file_extension, prefix):
    # 指定した拡張子のファイルパスを取得
    search_pattern = os.path.join(folder_path, f'*.{file_extension}')
    files = glob.glob(search_pattern)

    # ファイルが存在しない場合は終了
    if not files:
        print("指定された拡張子のファイルは見つかりませんでした。")
        return

    # 最新のファイルを見つける
    latest_file = max(files, key=os.path.getmtime)

    # 新しいファイル名を作成 (prefix + 元のファイル名)
    original_file_name = os.path.basename(latest_file)
    new_file_name = f"{prefix}{original_file_name}"
    new_file_path = os.path.join(folder_path, new_file_name)

    # リネームを実行
    os.rename(latest_file, new_file_path)
    print(f"{latest_file} を {new_file_path} にリネームしました。")

def delete_files_with_extension(folder_path, file_extension):
    # 指定した拡張子を持つファイルのパスを取得
    pattern = os.path.join(folder_path, f'*.{file_extension}')
    files_to_delete = glob.glob(pattern)

    # ファイルを削除
    for file_path in files_to_delete:
        try:
            os.remove(file_path)
            print(f'削除しました: {file_path}')
        except Exception as e:
            print(f'削除できませんでした: {file_path}. 理由: {e}')

if __name__ == "__main__":
    # 使用例
    folder_path = "folder_path"  # 対象のフォルダパス
    file_extension = "csv"              # 拡張子 (例: txt)
    test_number = "01"          # 新しいファイル名
    under_vbar = "_"

    rename_latest_file(folder_path, file_extension, test_number + under_vbar)