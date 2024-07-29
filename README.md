# Blot Photo Printer
![IMG_4508](https://github.com/user-attachments/assets/f9bb2bca-de72-45ba-a890-efc86e84a981)

1. Set the COM port in the index.js file on line 9
2. Install all node dependencies using `npm install`
3. Install Requests python library with command `pip install requests`
4. Install Pillow python library with command `pip install pillow`
5. Run the node server using `node .`
6. Set your `DOT_DIAMETER` in main.py to the size of the dot that your pen makes in millimeters
7. Set your `PUSH_COUNT` to the amount of times you want your pen to push against the paper for each dot. 1 is enough for sharpie, pencil leads might require up to 4 pushes or more
8. Set your `PRINTED_WIDTH` to the amount of dots you want your finished image to be in its width
9. Set your `INPUT_IMAGE` to the file name of the image you want to print using your Blot
10. Run the python script with command `python main.py` or `python3 main.py` for macOS/Linux
