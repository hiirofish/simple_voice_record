
# 音声録音プログラム

このプログラムは、Pythonを使用して簡単な音声録音機能を提供するGUIアプリケーションです。ユーザーは利用可能な入力デバイスを選択し、ボタン一つで録音の開始と停止を行うことができます。

## 機能

- 利用可能な入力デバイスのリストアップと選択
- ワンクリックでの録音開始/停止
- リアルタイムの録音時間表示
- WAVファイル形式での録音保存
- エラー情報とステータスのGUI表示

## 必要条件

- Python 3.6以上
- PyAudio
- tkinter (通常Pythonに標準搭載)

## インストール

1. 必要に応じてPyAudioをインストールします：

   ```
   pip install pyaudio
   ```

2. このリポジトリをクローンするか、`audio_recorder.py`ファイルをダウンロードします。

## 使用方法

1. コマンドラインで以下を実行します：

   ```
   python audio_recorder.py
   ```

2. アプリケーションウィンドウが開きます。
3. ドロップダウンメニューから使用したい入力デバイスを選択します。
4. 「録音」ボタンをクリックして録音を開始します。
5. 「停止」ボタンをクリックして録音を終了します。
6. 録音は自動的にWAVファイルとして保存されます。

## 注意事項

- 録音ファイルは、プログラムを実行したディレクトリに`recording_YYYYMMDD_HHMMSS.wav`の形式で保存されます。
- エラーが発生した場合は、アプリケーションウィンドウ内にエラーメッセージが表示されます。

## トラブルシューティング

- デバイスが認識されない場合は、システムの音声設定を確認してください。
- 録音に失敗する場合は、選択したデバイスが正しく機能しているか確認してください。
- 文字化けが発生する場合は、システムの言語設定を確認してください。

## ライセンス

このプロジェクトはMITライセンスの下で公開されています。