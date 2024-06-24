'''
Learn the basics of image processing using OpenCV
'''
import cv2

image_dir = "images/"
image_fname = "Macaws.jpg"
video_dir = "videos/"
video_fname = "The Hobbit Trailer Pop-Up - Lord of the Rings Movie.mp4"

def show_image(text, img):
    cv2.imshow(text, img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

def load_image(fname):
    '''Loads, displays, and returns an image'''
    img = cv2.imread(fname)
    cv2.imshow("Loaded Image", img)
    print(type(img))
    print(img.shape)
    cv2.waitKey(0)  #Wait for a keypress
    cv2.destroyAllWindows()
    return img

def show_colorspaces(img):
    '''Illustrate image in different color spaces'''
    gray_img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    show_image("Grayscale Image", gray_img)

    hsv_img = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    show_image("HSV Image", hsv_img)

    YCrCb_img =cv2.cvtColor(img, cv2.COLOR_BGR2YCrCb)
    show_image("YCrCb Image", YCrCb_img)

    cielab_img =cv2.cvtColor(img, cv2.COLOR_BGR2LAB)
    show_image("CIE LAB Image", cielab_img)

    cieluv_img =cv2.cvtColor(img, cv2.COLOR_BGR2LUV)
    show_image("CIE LUV Image", cieluv_img)


def blur_image(img):
    '''Display a blurred version of img'''
    blurred_img = cv2.GaussianBlur(img, (21, 21), 0)
    show_image("Blurred Image", blurred_img)


def show_edges(img):
    '''Display the edges in img using the Canny edge detector'''
    edge_img = cv2.Canny(img, 100, 200)  #Args are lower and upper thresholds for hysteresis
    show_image("Edge Image", edge_img)


def draw_lines(img):
    '''Draw lines on an image by modifying pixels'''
    copy = img.copy()
    copy[95:105, 45:55] = [255, 0, 0]  #Set a small square of pixels to blue
    cv2.imshow("Modified Image", copy)
    extraction = copy[75:125, 25:75]  #Extract a small area around the modified pixels
    cv2.imshow("Extracted Image", extraction)  #Display the extracted region
    cv2.waitKey(0)
    height, width, channels = copy.shape  #Get the image dimensions
    mid_col = width//2  #Find the middle column
    mid_row =height//2  #Find the middle row
    copy[:, mid_col] = [0, 0, 255]  #Draw a vertical red line down the center
    # Or, to draw a thicker line: 
    # copy[:, mid_col-5:mid_col+5] = [0, 0, 255]
    #Add a green horizontal line across the middle of the image
    copy[mid_row, :] = [0, 255, 0]  
    show_image("Vertical and Horizontal Line", copy)


def play_video(fname):
    '''Plays the image frames from a video; does not play audio'''
    cap = cv2.VideoCapture(fname)  #Create a capture object
    if cap.isOpened():
        while True:
            ret, frame = cap.read()  #Read the return value and the frame
            if not ret:
                break  #Break the loop when the video ends
            cv2.imshow("Video Frame", frame)
            if cv2.waitKey(25) & 0xFF == ord('q'):
                break  #Quit the video on 'q' key
    else:
        print("Error: Unable to open the video file")
    cap.release()
    cv2.destroyAllWindows()


def diff_frames(fname):
    '''Displays the differences between video frames; toggle on 'd' key'''
    show_diff = False  #Determines whether to display the frame or the diff
    cap = cv2.VideoCapture(fname)
    if cap.isOpened:
        ret, prev_frame = cap.read()  #Read first frame
        while True:
            ret, frame = cap.read()
            if not ret:
                break  #Break loop when video ends
            if show_diff:
                frame_diff = cv2.absdiff(prev_frame, frame)
                cv2.imshow("Video Frame", frame_diff)
            else:
                cv2.imshow("Video Frame", frame)
            prev_frame = frame
            key = cv2.waitKey(25)  #Wait 25 ms for a key press
            if key & 0xFF == ord('d'):
                if show_diff:
                    show_diff = False
                else:
                    show_diff = True
            elif key & 0xFF == ord('q'):
                break  #Quit the video on 'q' key
    else:
        print("Error: Unable to open the video file")
    cap.release()
    cv2.destroyAllWindows()


def main():
    filename = image_dir + image_fname
    img = load_image(filename)
    show_colorspaces(img)
    blur_image(img)
    show_edges(img)
    draw_lines(img)
    play_video(video_dir + video_fname)
    diff_frames(video_dir + video_fname)

main()
