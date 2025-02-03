import cv2
import numpy as np

class Tracker:
    def __init__(self):
        self.cap = cv2.VideoCapture(0)
        self.roi_selected = False
        self.drawing = False
        self.roi_start = (0, 0)
        self.roi_end = (0, 0)
        self.tracker = None  # Initialize tracker as None
        self.tracking_initialized = False
        self.bbox = None
        self.crosshair_size = 20
        self.target_color = (0, 255, 0)  # Green color for tracking
        self.min_selection_size = 20  # Minimum selection size

    def create_tracker(self):
        # Try different tracker - MOSSE is more stable for initialization
        return cv2.legacy.TrackerMOSSE_create()

    def mouse_callback(self, event, x, y, flags, param):
        if event == cv2.EVENT_LBUTTONDOWN:
            self.drawing = True
            self.roi_start = (x, y)
            self.roi_selected = False
        elif event == cv2.EVENT_MOUSEMOVE and self.drawing:
            self.roi_end = (x, y)
        elif event == cv2.EVENT_LBUTTONUP:
            self.drawing = False
            self.roi_end = (x, y)
            self.roi_selected = True

    def draw_crosshair(self, frame, x, y, w, h):
        """Draw professional camera-style crosshair and box"""
        center_x = x + w // 2
        center_y = y + h // 2
        
        # Draw center crosshair
        cv2.line(frame, (center_x - self.crosshair_size, center_y),
                (center_x + self.crosshair_size, center_y), self.target_color, 1)
        cv2.line(frame, (center_x, center_y - self.crosshair_size),
                (center_x, center_y + self.crosshair_size), self.target_color, 1)
        
        # Draw tracking box
        cv2.rectangle(frame, (x, y), (x + w, y + h), self.target_color, 2)
        
        # Draw corner markers
        marker_length = 10
        # Top left
        cv2.line(frame, (x, y), (x + marker_length, y), self.target_color, 2)
        cv2.line(frame, (x, y), (x, y + marker_length), self.target_color, 2)
        # Top right
        cv2.line(frame, (x + w, y), (x + w - marker_length, y), self.target_color, 2)
        cv2.line(frame, (x + w, y), (x + w, y + marker_length), self.target_color, 2)
        # Bottom left
        cv2.line(frame, (x, y + h), (x + marker_length, y + h), self.target_color, 2)
        cv2.line(frame, (x, y + h), (x, y + h - marker_length), self.target_color, 2)
        # Bottom right
        cv2.line(frame, (x + w, y + h), (x + w - marker_length, y + h), self.target_color, 2)
        cv2.line(frame, (x + w, y + h), (x + w, y + h - marker_length), self.target_color, 2)

        # Draw dimensions
        cv2.putText(frame, f'{w}x{h}px', (x + w + 10, y + h//2),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.6, self.target_color, 1)

    def run(self):
        cv2.namedWindow('Tracker')
        cv2.setMouseCallback('Tracker', self.mouse_callback)

        while True:
            ret, frame = self.cap.read()
            if not ret:
                break

            display_frame = frame.copy()
            gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)  # Create grayscale version

            if self.drawing:
                # Draw professional selection box while dragging
                x = min(self.roi_start[0], self.roi_end[0])
                y = min(self.roi_start[1], self.roi_end[1])
                w = abs(self.roi_start[0] - self.roi_end[0])
                h = abs(self.roi_start[1] - self.roi_end[1])
                self.draw_crosshair(display_frame, x, y, w, h)

            if self.roi_selected:
                try:
                    x = min(self.roi_start[0], self.roi_end[0])
                    y = min(self.roi_start[1], self.roi_end[1])
                    w = abs(self.roi_start[0] - self.roi_end[0])
                    h = abs(self.roi_start[1] - self.roi_end[1])
                    
                    # Check minimum size and maximum size
                    if w > self.min_selection_size and h > self.min_selection_size:
                        self.bbox = (x, y, w, h)
                        self.tracker = self.create_tracker()
                        
                        # Initialize tracker with grayscale frame
                        ok = self.tracker.init(gray_frame, self.bbox)
                        
                        if ok:
                            self.tracking_initialized = True
                            print(f"Tracker initialized successfully: box={self.bbox}")
                        else:
                            print("Tracker initialization failed - try selecting a different area")
                            self.tracking_initialized = False
                    else:
                        print(f"Selection too small: {w}x{h}, minimum size is {self.min_selection_size}")
                        cv2.putText(display_frame, "Selection too small!", (10,90), 
                                  cv2.FONT_HERSHEY_SIMPLEX, 0.75,(0,0,255),2)
                except Exception as e:
                    print(f"Error initializing tracker: {e}")
                    self.tracking_initialized = False
                self.roi_selected = False

            if self.tracking_initialized and self.tracker is not None:
                try:
                    # Update tracker with grayscale frame
                    ok, bbox = self.tracker.update(gray_frame)
                    if ok:
                        self.bbox = bbox
                        x, y, w, h = [int(v) for v in bbox]
                        self.draw_crosshair(display_frame, x, y, w, h)
                        cv2.putText(display_frame, f"TRACKING ({x},{y})", (10,70), 
                                  cv2.FONT_HERSHEY_SIMPLEX, 0.75, self.target_color, 2)
                    else:
                        cv2.putText(display_frame, "TARGET LOST", (10,70), 
                                  cv2.FONT_HERSHEY_SIMPLEX, 0.75, (0,0,255), 2)
                        self.tracking_initialized = False
                except Exception as e:
                    print(f"Error updating tracker: {e}")
                    self.tracking_initialized = False

            # Add professional overlay
            cv2.putText(display_frame, "TARGET ACQUISITION", (10,30), 
                       cv2.FONT_HERSHEY_SIMPLEX, 0.75, self.target_color, 2)
            cv2.putText(display_frame, "[R] RESET  [Q] QUIT", (10,50), 
                       cv2.FONT_HERSHEY_SIMPLEX, 0.75, self.target_color, 2)

            cv2.imshow('Tracker', display_frame)
            
            key = cv2.waitKey(1) & 0xFF
            if key == ord('q'):
                break
            elif key == ord('r'):
                self.tracking_initialized = False
                self.roi_selected = False
                self.bbox = None
                self.tracker = None
                print("Tracker reset")

        self.cap.release()
        cv2.destroyAllWindows()

if __name__ == '__main__':
    tracker = Tracker()
    tracker.run()
