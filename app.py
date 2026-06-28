import streamlit as st
import csv
import re
import os

# これまでと同じ入力チェックの関数
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
    # ページのタイトル
    st.title('お客様データ入力フォーム')
    st.write('必要事項を入力して「登録」ボタンを押してください。')

    # 入力フォームの作成
    with st.form(key='registration_form'):
        user_id = st.text_input('ID (半角英数16文字まで)', max_chars=16)
        
        # パスワードは入力文字が隠れるように type='password' を指定
        pw = st.text_input('PW (半角英数16文字まで)', max_chars=16, type='password')
        
        name = st.text_input('名前 (全角半角16文字まで)', max_chars=16)
        event = st.text_input('種目 (3 または 4)')
        
        # 登録ボタン
        submit_button = st.form_submit_button(label='登録')

    # 登録ボタンが押されたあとの処理
    if submit_button:
        errors = []
        
        # エラーチェック
        if not is_valid_alphanumeric(user_id, 16):
            errors.append('IDは半角英数16文字以内で入力してください。')
        if not is_valid_alphanumeric(pw, 16):
            errors.append('PWは半角英数16文字以内で入力してください。')
        if not is_valid_name(name, 16):
            errors.append('名前は16文字以内で入力してください。')
        if not is_valid_event(event):
            errors.append('種目は 3 または 4 を半角で入力してください。')

        if errors:
            # エラーがある場合はすべて赤色の警告メッセージで表示
            for error in errors:
                st.error(error)
        else:
            # エラーがない場合はCSVファイルに書き込み
            csv_file_path = 'registration_data.csv'
            
            if not os.path.exists(csv_file_path):
                with open(csv_file_path, mode='w', newline='', encoding='cp932') as f:
                    pass
            
            try:
                with open(csv_file_path, mode='a', newline='', encoding='cp932') as file:
                    writer = csv.writer(file)
                    writer.writerow([user_id, pw, name, event])
                
                # 成功した場合は緑色のメッセージを表示
                st.success(f'登録が完了しました！ (ID: {user_id})')
                
            except Exception as e:
                st.error(f'ファイルの保存中にエラーが発生しました: {e}')

if __name__ == '__main__':
    main()