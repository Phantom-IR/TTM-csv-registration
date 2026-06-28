import streamlit as st
from github import Github
import base64
import re

def is_valid_alphanumeric(text, max_length):
    if len(text) > max_length or len(text) == 0:
        return False
    return bool(re.match(r'^[a-zA-Z0-9]+$', text))

def is_valid_name(text, max_length):
    if len(text) > max_length or len(text) == 0:
        return False
    return True

def is_valid_event(text):
    return text in ['3', '4']

def main():
    st.title('お客様データ入力フォーム')
    st.write('必要事項を入力して「登録」ボタンを押してください。')

    with st.form(key='registration_form'):
        user_id = st.text_input('ID (半角英数16文字まで)', max_chars=16)
        pw = st.text_input('PW (半角英数16文字まで)', max_chars=16, type='password')
        name = st.text_input('名前 (全角半角16文字まで)', max_chars=16)
        event = st.text_input('種目 (3 または 4)')
        
        submit_button = st.form_submit_button(label='登録')

    if submit_button:
        errors = []
        
        if not is_valid_alphanumeric(user_id, 16):
            errors.append('IDは半角英数16文字以内で入力してください。')
        if not is_valid_alphanumeric(pw, 16):
            errors.append('PWは半角英数16文字以内で入力してください。')
        if not is_valid_name(name, 16):
            errors.append('名前は16文字以内で入力してください。')
        if not is_valid_event(event):
            errors.append('種目は 3 または 4 を半角で入力してください。')

        if errors:
            for error in errors:
                st.error(error)
        else:
            try:
                # 1. GitHubへ接続
                g = Github(st.secrets["github"]["token"])
                
                # 【重要】ご自身のGitHubユーザー名とリポジトリ名に書き換えてください
                repo = g.get_repo("あなたのユーザー名/リポジトリ名") 
                
                file_path = "registration_data.csv"
                
                # 2. 現在のCSVファイルの内容を取得してデコード (Shift-JIS)
                contents = repo.get_contents(file_path)
                current_content = base64.b64decode(contents.content).decode('cp932')
                
                # 3. 新しいデータを末尾に追加
                new_row = f"{user_id},{pw},{name},{event}\n"
                updated_content = current_content + new_row
                
                # 4. GitHub上のファイルを更新（コミット）
                commit_message = f"Add new user data: {user_id}"
                repo.update_file(
                    contents.path,
                    commit_message,
                    updated_content.encode('cp932'), # Shift-JISに戻して保存
                    contents.sha
                )
                
                st.success(f'登録が完了しました！ (ID: {user_id})')
                
            except Exception as e:
                st.error(f'ファイルの保存中にエラーが発生しました: {e}')

if __name__ == '__main__':
    main()
