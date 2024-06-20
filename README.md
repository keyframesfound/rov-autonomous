# ROV Autonomous
<img src="https://marinesanctuary.org/wp-content/uploads/2020/04/FGB_DFH24_gps-19-scaled.jpg" width="600" height="400">

## Description
The **ROV Autonomous** project is developed by the St Stephen's College (Underwater ROV) Team for the international ROV Mate competition in underwater robotics. Our goal is to create an autonomous underwater vehicle (ROV) combining the advanced image processing of computer vision, real-time feedback for easy and precise manoeuvring, and precise autonomous navigation capabilities. We are creating a less processor-intensive task to open up live and real-time autonomous piloting for any operator with a simple computer.


## Features

1. **Red Square Detection**:
   - Our software uses image processing techniques to identify 15x15 red squares underwater. This feature is crucial for detecting specific locations of interest, such as submerged markers, which is part of the ROV tasks of the International Mate Competition. 
<img src="https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcS7jm39EZ-Mjt60lizqK9fqTnQDf_W-jfGaig&s" width="600" height="400">



2. **Real-Time Feedback**:
   - Real-time feedback is for precise control when underwater, water currents, props and others are a large and genuine threat to our underwater ROV. We can transmit real-time updates to the piloting team regarding the current ROV situation using real-time autonomous feedback. Our system provides pilots real-time information about the ROV's position, orientation, and surrounding conditions. Whether adjusting thrusters or avoiding obstacles would be the best course of action, operators can make decisions within seconds to deal with problems that have arisen.



3. **Underwater Navigation**:
   - Navigating underwater environments presents unique challenges. Our autonomous navigation system leverages depth sensors, compass data, and obstacle avoidance algorithms to guide the ROV through rough water areas safely. 


## Installation
1. **Clone the Repository**:
   - Open your terminal or command prompt.
   - Navigate to the directory where you want to store your local copy of the repository.
   - Run the following command to clone the repository:
     ```
     git clone https://github.com/keyframesfound/rov-autonomous.git
     ```

2. **Install Dependencies**:
   - Ensure that you have Python installed on your system.
   - Navigate to the cloned repository folder:
     ```
     cd rov-autonomous
     ```

3. **Configure Your Environment**:
   - If necessary, create a virtual environment to isolate the project dependencies:
     ```
     python -m venv myenv
     ```
   - Activate the virtual environment:
     - On Windows:
       ```
       myenv\Scripts\activate
       ```
     - On macOS and Linux:
       ```
       source myenv/bin/activate
       ```

4. **Run the Main Script**:
   - Execute the main script to start the ROV Autonomous system:
     ```
     python main.py
     ```

## Recommended Hardware

To get the most out of the **ROV Autonomous** software, consider using the following hardware components:

- **ROV Platform**: Choose a robust underwater vehicle platform with good maneuverability. Look for models that allow easy integration of sensors and cameras.
- **Camera System**: Invest in a high-resolution camera system with low-light capabilities. A camera with adjustable focus and exposure settings is ideal.
- **Depth Sensor**: Install a reliable depth sensor to help the ROV maintain its position and avoid collisions.
- **Microcontroller or Single-Board Computer (SBC)**: Use a powerful microcontroller or SBC (e.g., Raspberry Pi, NVIDIA Jetson) to run the software.
- **Thrusters and Motors**: Select efficient thrusters and motors for precise movement control.

## Compatible Software

The **ROV Autonomous** software works seamlessly with the following tools and libraries:

- **OpenCV**: Used for image processing and red square detection.
- **Python**is the primary programming language for the software.
- **ROS (Robot Operating System)**: If you're building a more complex ROV system, consider integrating with ROS for communication between different components.
- **GStreamer**: For streaming real-time video from the camera to the operator's interface.

## Usefulness and Applications

The **ROV Autonomous** software has several practical applications:

1. **Underwater Inspections**: Use the ROV to inspect underwater structures, pipelines, and marine ecosystems. The red square detection feature can help identify specific objects of interest.
2. **Search and Rescue**: Deploy the ROV in emergency situations to search for missing persons or retrieve objects from underwater locations.
3. **Scientific Research**: Researchers can study marine life, underwater habitats, and geological formations using the autonomous ROV.
4. **Environmental Monitoring**: Monitor pollution levels, track changes in underwater environments, and collect data for conservation efforts.

By combining hardware, software, and real-time feedback, the **ROV Autonomous** project empowers users to explore and interact with the underwater world more effectively.

## Inspirations and Similar Projects

Here are some inspiring projects and developments related to AUVs and ROVs:

1. **Armada by Ocean Infinity**:
   - Ocean Infinity, a subsea survey company, launched a subsidiary called Armada. Armada specializes in producing automated surface vessels carrying subsea ROVs. These vessels can be used for underwater inspection.

2. **Fugro and Sea-Kit International**:
   - Geological survey company Fugro is collaborating with Sea-Kit International to develop drone ships. These ships aim to minimize or eliminate the dependency on support vessels and umbilicals, making them more autonomous. Improved flexibility during offshore inspections and enhanced worker safety are key benefits of such autonomous vessels.


: [Offshore Technology: Will 2020 be the year of ROV and vessel automation?](https://www.offshore-technology.com/features/vessel-automated-uavs-rovs-offshore/)
: [Wikipedia: Autonomous underwater vehicle](https://en.wikipedia.org/wiki/Autonomous_underwater_vehicle)

## Contributing

Contributions are welcome! Please open an issue or submit a pull request.
