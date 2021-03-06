# Get in IT: Code and Win
This is my solution for the get in IT coding challenge 2020/21.
Further information can be found on the get-in-it page: https://www.get-in-it.de/coding-challenge
<br>
The submission deadline was January 10th, 2021, so the project has not been maintained since then.
<br>
EDIT: I got the 3rd place! 🎉

## The Task
The task was to drive two trucks to a location in Bonn and only have a limited capacity to deal with different devices as effectively as possible. The devices differ in "utility" value, weight and the required number in Bonn. The "utility" value indicates how urgently a certain device is needed. The devices and their values can be viewed here: https://www.get-in-it.de/imgs/it/codingCompetition/bwi/code_for_bwi.pdf
<br>
The weight of the driver, must be deducted from the total capacity of the truck.
<br><br>
### Underlying Problem
This task is based on the so-called "bagpack" problem, which is one of the most complicated in computer science. In order to really get the most effective loading, an algorithm with a very long runtime is required, which also depend on the number of elements that have to be sorted. In this algorithm all possible combinations are checked and then the most effective is returned. I can recommend this solution for tasks with a small number of elements.
<br>
<br>
### My Algorithm
In order to load the trucks as effectively as possible, I used a heuristic approach and implemented a simple variant of the greedy algorithm. The greedy algorithm is characterized by its short runtime and comparatively good results.
<br>
<br>
First, the devices are sorted in descending order according to their effectiveness (in database.py):
<br>
```
data = self.fetchall('SELECT * FROM devices ORDER BY weight/benefit')
```
<br>
The effectiveness of a device is determined by the ratio between weight and utility. The formula for this is:
<code>effectiveness = weight / utility value</code>
<br><br>
After sorting, the devices are packed into the truck, starting with the most effective. Depending on how much space is still available in the truck, not all units of a device are packed, or the algorithm jumps to the next element.
<br>
This results in the following loading lists:

<table>
<tr><th>TRANSPORTER NR.1</th><th>TRANSPORTER NR.2</th></tr>
<tr><td>
  
| Device                  | Units |
| ----------------------- |-------|
| Mobiltelefon Outdoor    | 157   |
| Mobiltelefon Heavy Duty | 220   |
| Mobiltelefon Büro       | 60    |
| Tablet outdoor groß     | 283   |
> total utility value: 44764<br>free capacity: 724 g

</td><td>
  
| Device              | Units |
| ------------------- |-------|
| Tablet outdoor groß | 87    |
| Tablet Büro klein   | 599   |
> total utility value: 29876<br>free capacity: 445 g

</td></tr></table>

## The Program

### Installation
After you have downloaded the project you have to install all required packages with:
<br>
```
pip install -r requirements.txt
```

The program is written in Python, so make sure you have Python3 installed.
<br>Enter the following command to start the program:
```
python main.py
```
<br>

### Description
My application basically consists of two areas. One is the area for editing the database entries for devices, transporter and drivers, as well as creating the loading lists. And secondly, the delivery game area in which the user has the task of collecting the packages with his truck. The second area (game area) was not part of the requirements.

### GUI first area:
![alt text](https://github.com/FinnMal/getinit_code_and_win/blob/main/assets/img/first_area.png?raw=true)

After pressing on "Geräte bearbeiten" (edit devices) you see this:
<br>

![alt text](https://github.com/FinnMal/getinit_code_and_win/blob/main/assets/img/first_area_devices.png?raw=true)


When you click on "Ladeliste erstellen". The button "Ausliefern" (deliver) becomes visible. This leads you to ...

## The Delivery Game
The delivery game wasn't part of the task.
<br>
The aim of the game is to collect all the packages from the loading list and not cause an car accident. The counters above show how many units of the various devices have already been collected. Once all the packages have been collected, you can switch to the next transporter.


![alt text](https://github.com/FinnMal/getinit_code_and_win/blob/main/assets/img/delivery_game_demo.gif?raw=true)


### Controls
| Key                                 | Function                          |
| ----------------------------------- |-----------------------------------|
| <code>Left</code> / <code>A</code>  | steer truck one lane to the left  |
| <code>Right</code> / <code>D</code> | steer truck one lane to the right |
| <code>Up</code> /<code>W</code>     | increase the speed of the truck   |
| <code>Down</code> / <code>S</code>  | decreace the speed of the truck   |

#### In the info box
| Key                                   | Function                     |
| ------------------------------------- |------------------------------|
| <code>Left</code>/<code>A</code>      | Move one button to the left  |
| <code>Right</code>/<code>D</code>     | Move one button to the right |
| <code>Space</code>/<code>Enter</code> | Press the selected button    |
