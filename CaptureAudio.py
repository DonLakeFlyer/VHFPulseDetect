import sounddevice as sd

def main():
	duration = 10  # seconds
	sampleRate = 128000
	myrecording = sd.rec(int(duration * sampleRate), samplerate=sampleRate, channels=1, blocking=True)
	print(len(myrecording))

if __name__ == '__main__':
    main()
