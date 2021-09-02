# Smart-Aquarium
A 24/7 watch and alert system for freshwater home aquariums.

## Objective:
The purpose of this project is to design and prototype a “watch and alert” system that will allow an aquarist to travel for short periods of time without worrying unnecessarily that the aquarium inhabitants are in danger. It will also alert the user when something undesiring occurs in the aquarium via website, app, and email. The user will interact with the device via a website or phone app by having live data 24/7 of the status of the tank such as: current water temperature and water levels. The user will also be able to control the timing of lighting and testing of water parameters, such as ammonia and pH, by changing the settings manually on the app. By default, the device will automatically monitor and adjust these settings by using preprogrammed settings set by the user. If there is a power outage, the user will have less to worry about, as the device will also have a backup battery that will continue powering the two most important components tasked with keeping the inhabitants alive, the aquarium filter and aerator. The device will send alerts to the user when the power backup is enabled and how much power is left before the backup power also runs out. It is desired to include a “recommendation system” that will offer course of actions to the end user through the app and the website according to the state of the aquarium. The lighting conditions that we are trying to do, is to simulate current lighting conditions according to zip code. And finally, integrate a “top off” system that keeps the water level at an ideal height. 

## Special Considerations:
- In this project, we’re going to assume that the smart aquarium is going to be used in an environment that has Wi-Fi.
- This project will be built around a small (2-5) gallon aquarium; thus, the lighting will be constrained to the size of the corresponding aquarium hood.

## System Design:
Level 0 design: Shows the inputs and outputs of the system.
![image](https://user-images.githubusercontent.com/70276800/131925922-6bad2357-2850-4557-ba60-1aa129ff0238.png)

Level 1 design: demonstrates a closer look inside level 0 design. Level 1 shows the 3 main modules for this system.
![image](https://user-images.githubusercontent.com/70276800/131925932-601013a4-177b-4924-a975-cd9b2b020607.png)

Level 3 design: demonstrates a detailed view of the components that make-up the power module.
![image](https://user-images.githubusercontent.com/70276800/131926346-b681dc6c-d6f2-43a2-ac0a-4f98742f233f.png)





