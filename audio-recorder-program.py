import pyaudio
import wave
import tkinter as tk
import threading
import datetime
import time
import traceback

class AudioRecorder:
    def __init__(self, master):
        self.master = master
        master.title("音声録音プログラム")
        
        # ウィンドウサイズを設定（必要に応じて調整）
        master.geometry("600x300")
        
        # フォントスタイルを設定
        self.font_style = ("Arial", 24)
        
        # ボタンを作成
        self.button = tk.Button(master, text="録音", command=self.toggle_recording,
                                font=self.font_style, width=12, height=2)
        self.button.pack(pady=40)
        
        # ラベルを作成
        self.label = tk.Label(master, text="録音時間: 0.0 秒", font=self.font_style)
        self.label.pack()
        
        self.is_recording = False
        self.frames = []
        self.start_time = None
        
        self.CHUNK = 1024
        self.FORMAT = pyaudio.paInt16  # 16ビット
        self.CHANNELS = 1              # モノラル
        self.RATE = 44100              # サンプリングレート（Hz）
        
        self.p = pyaudio.PyAudio()
        
        # デバイスインデックスを初期化
        self.device_index = None
        self.list_input_devices()
        
        # アプリケーション終了フラグ
        self.is_closing = False
        
    def list_input_devices(self):
        print("利用可能な入力デバイス:")
        for i in range(self.p.get_device_count()):
            info = self.p.get_device_info_by_index(i)
            if info['maxInputChannels'] > 0:
                print(f"デバイス {i}: {info['name']}")
                # 必要に応じてUSBマイクを自動選択
                if 'USB' in info['name'] or 'Microphone' in info['name']:
                    self.device_index = i
        if self.device_index is None:
            print("USBマイクが見つかりませんでした。デフォルトの入力デバイスを使用します。")
        
    def toggle_recording(self):
        if not self.is_recording:
            self.start_recording()
        else:
            self.stop_recording()
        
    def start_recording(self):
        self.is_recording = True
        self.button.config(text="停止")
        self.frames = []
        self.start_time = time.time()
        
        # 録音スレッドの開始
        self.record_thread = threading.Thread(target=self.record)
        self.record_thread.daemon = True
        self.record_thread.start()
        
        # ラベルの更新を開始
        self.update_label()
        
    def record(self):
        try:
            stream = self.p.open(format=self.FORMAT,
                                 channels=self.CHANNELS,
                                 rate=self.RATE,
                                 input=True,
                                 input_device_index=self.device_index,
                                 frames_per_buffer=self.CHUNK)
        except Exception as e:
            print(f"ストリームを開く際のエラー: {e}")
            traceback.print_exc()
            self.is_recording = False
            self.button.config(text="録音")
            return
        
        while self.is_recording and not self.is_closing:
            try:
                data = stream.read(self.CHUNK, exception_on_overflow=False)
                self.frames.append(data)
            except Exception as e:
                print(f"ストリーム読み取り中のエラー: {e}")
                traceback.print_exc()
                break
        
        stream.stop_stream()
        stream.close()
        
    def stop_recording(self):
        self.is_recording = False
        self.button.config(text="録音")
        if self.record_thread.is_alive():
            self.record_thread.join(timeout=1)
        if self.frames:
            print(f"録音フレーム数: {len(self.frames)}")
            self.save_audio()
        else:
            print("録音された音声がありません。")
        
    def update_label(self):
        if self.is_recording:
            elapsed_time = time.time() - self.start_time
            self.label.config(text=f"録音時間: {elapsed_time:.1f} 秒")
            self.master.after(100, self.update_label)
        else:
            self.label.config(text="録音時間: 0.0 秒")
        
    def save_audio(self):
        current_time = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        self.filename = f"recording_{current_time}.wav"
        
        wf = wave.open(self.filename, 'wb')
        wf.setnchannels(self.CHANNELS)
        wf.setsampwidth(self.p.get_sample_size(self.FORMAT))
        wf.setframerate(self.RATE)
        wf.writeframes(b''.join(self.frames))
        wf.close()
        
        print(f"録音を保存しました: {self.filename}")
        
        # ここで wave モジュールを使用してファイル属性を表示
        self.show_wave_info()
        
    def show_wave_info(self):
        try:
            with wave.open(self.filename, 'rb') as wf:
                channels = wf.getnchannels()
                sample_width = wf.getsampwidth()
                framerate = wf.getframerate()
                num_frames = wf.getnframes()
                duration = num_frames / float(framerate)
                
                # サンプル幅をビットに変換
                precision = sample_width * 8
                
                # ファイルサイズを取得
                file_size = os.path.getsize(self.filename)
                
                # ビットレートを計算
                bit_rate = framerate * precision * channels
                
                # ファイルサイズを適切な単位に変換
                if file_size >= 1024 * 1024:
                    size_unit = "M"
                    file_size_display = f"{file_size / (1024 * 1024):.1f}{size_unit}"
                elif file_size >= 1024:
                    size_unit = "k"
                    file_size_display = f"{file_size / 1024:.1f}{size_unit}"
                else:
                    size_unit = "B"
                    file_size_display = f"{file_size}{size_unit}"
                
                # 時間を表示形式に変換
                duration_minutes = int(duration // 60)
                duration_seconds = duration % 60
                duration_display = f"{duration_minutes:02d}:{duration_seconds:05.2f}"
                
                print("録音したファイルの属性:")
                print(f"Input File     : '{self.filename}'")
                print(f"Channels       : {channels}")
                print(f"Sample Rate    : {framerate}")
                print(f"Precision      : {precision}-bit")
                print(f"Duration       : {duration_display} = {num_frames} samples")
                print(f"File Size      : {file_size_display}")
                print(f"Bit Rate       : {bit_rate / 1000:.1f}k")
                print("Sample Encoding: 16-bit Signed Integer PCM")
        except Exception as e:
            print(f"ファイル情報の取得中に例外が発生しました: {e}")
            traceback.print_exc()
        
    def on_closing(self):
        self.is_closing = True
        if self.is_recording:
            self.stop_recording()
        self.p.terminate()
        self.master.destroy()

import os  # os モジュールを追加

if __name__ == '__main__':
    root = tk.Tk()
    recorder = AudioRecorder(root)
    root.protocol("WM_DELETE_WINDOW", recorder.on_closing)
    root.mainloop()
