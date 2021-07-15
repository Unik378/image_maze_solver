from PIL import Image

def createGIF(path,frameCount):
    inp = Image.open(path)
    out  = Image.open('./output/output.jpg')
    frames = []

    for i in range(frameCount):
        img = Image.open('./frames/'+str(i)+'.jpg')
        frames.append(img)
    
    time = 3000
    duration = time/len(frames)

    x = 0
    while x < 500:
        frames.append(out)
        x += duration

    inp.save('./output/out.gif',save_all=True, append_images=frames, optimize=False, duration=duration, loop=0)