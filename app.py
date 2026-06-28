import streamlit as st
import csv
import re
import os

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

def get_next_id(csv_file_path):
    # ファイルがない場合は最初のIDを返す
    if not os.path.exists(csv_file_path):
        return "10001"
    
    last_id = 10000
    try:
        # CSVファイルを読み込んで一番最後のIDを探す
        with open(csv_file_path, mode='r', encoding='cp932') as f:
            reader = csv.reader(f)
            for row in reader:
                # 空行をスキップし、1列目が数値のデータを探す
                if row and row[0].isdigit():
                    last_id = int(row[0])
    except Exception:
        pass
        
    # 最後のIDに1を足したものを新しいIDとする
    return str(last_id + 1)

def main():
    st.title('お客様データ入力フォーム')
    st.write('必要事項を入力して「登録」ボタンを押してください。')

    with st.form(key='registration_form'):
        # お客様に入力させるID欄を削り、案内文に変更
        st.write('※IDは登録完了時に自動的に割り当てられます。')
        
        pw = st.text_input('PW (半角英数16文字まで)', max_chars=16, type='password')
        name = st.text_input('名前 (全角半角16文字まで)', max_chars=16)
        event = st.text_input('種目 (3 または 4)')
        
        submit_button = st.form_submit_button(label='登録')

    if submit_button:
        errors = []
        
        # IDの検証処理を削除し、その他の項目のみ検証
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
            csv_file_path = 'registration_data.csv'
            
            # ここで自動的に新しい連番IDを生成する
            user_id = get_next_id(csv_file_path)
            
            if not os.path.exists(csv_file_path):
                with open(csv_file_path, mode='w', newline='', encoding='cp932') as f:
                    pass
            
            try:
                with open(csv_file_path, mode='a', newline='', encoding='cp932') as file:
                    writer = csv.writer(file)
                    writer.writerow([user_id, pw, name, event])
                
                # 成功メッセージに自動生成されたIDを表示してお客様に伝える
                st.success(f'登録が完了しました！ (あなたのID: {user_id})')
                
            except Exception as e:
                st.error(f'ファイルの保存中にエラーが発生しました: {e}')

if __name__ == '__main__':
    main()
