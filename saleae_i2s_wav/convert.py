import wave
import sys

# One sample is one frame is one left word + one right word

def ConvertFile(filename_in:str, filename_out:str="out.wav", nChannels:int=2, sample_width:int=4, freq:int=None):
    with open(filename_in, 'r') as inFile, wave.open(filename_out, 'wb') as wavFile:
        header = inFile.readline()
        # Calculate the frequency if it is not specified
        if freq is None:
            time_step1 = float(inFile.readline().split(',')[0])
            time_step2 = float(inFile.readline().split(',')[0])
            # Round to the nearest 100Hz, variable unit is still Hz though
            freq = round(1 / ((time_step2 - time_step1) * 200)) * 100
            print(f"Calculated frequency: {freq}")
            
            inFile.seek(0) # Move back to top of file
            inFile.readline() # Move past the header row
        
        # Print out settings
        print(f"Converting {filename_in} to {filename_out}...")
        print(f"\tSample Width: {sample_width}")
        print(f"\t# Channels: {nChannels}")
        print(f"\tSample Freq: {freq}")

        # Set wave file header
        wavFile.setnchannels(nChannels)
        wavFile.setsampwidth(sample_width)
        wavFile.setframerate(freq)

        word_len = int(sample_width / nChannels)

        # Convert text to wave frames
        lineNum = 1
        try:
            while True:
                # Read line 1
                row1 = inFile.readline()
                if not row1 or row1 == '': break #EOF
                lineNum += 1
                row1 = row1.split(',')

                # Get row 1 data
                channel1 = int(row1[1])
                data1 = int(row1[2])
                bdata1 = data1.to_bytes(word_len, 'little', signed=True)
                
                if (nChannels == 2):
                    # Read line 2
                    row2 = inFile.readline()
                    if not row2 or row2 == '': break #EOF
                    lineNum += 1
                    row2 = row2.split(',')

                    # Get row 2 data
                    channel2 = int(row2[1])
                    data2 = int(row2[2])
                    bdata2 = int.to_bytes(data2, word_len, 'little', signed=True)

                    # Rearrange the words if needed and write frame
                    if channel1 < channel2:
                        # channels are normal
                        wavFile.writeframes(bdata1 + bdata2)
                    else:
                        # channels are flipped
                        wavFile.writeframes(bdata2 + bdata1)

                # Assume monochannel
                else:
                    wavFile.writeframes(bdata1)

        except Exception as e:
            print(f"Exception {e} at line {lineNum} in file {filename_in}")
            




if __name__ == "__main__":
    # Check for correct number of args
    usage_str = """Usage: python3 convert.py input_file output_file"""
    if len(sys.argv) < 2:
        print(usage_str)
        exit()

    if len(sys.argv) >= 3:
        ConvertFile(sys.argv[1], sys.argv[2])
    else:
        ConvertFile(sys.argv[1])
    
