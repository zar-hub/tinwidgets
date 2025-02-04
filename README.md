<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Braah+One&family=Rampart+One&family=Rubik+Mono+One&display=swap" rel="stylesheet">
<style>
.rampart-one-regular {
  font-family: "Rampart One", serif;
  font-weight: 400;
  font-style: normal;
}
.braah-one-regular {
  font-family: "Braah One", serif;
  font-weight: 400;
  font-style: normal;
}
.rubik-mono-one-regular {
  font-family: "Rubik Mono One", serif;
  font-weight: 400;
  font-style: normal;
}
body{
  background: #2B2B2B;
}
.gears-container{
    width: 50px; 
    height: 45px;
    font-size:24px;
    padding: 9%;
    position: relative; 
    margin: 0px auto;
    border: solid
}
.gear-rotate{
	width: 2em;
	height: 2em;
  top: 48%; 
  left: 47%; 
	background: #E9E581;
	position: absolute;
	border-radius: 1em;
  z-index: -1;
	-webkit-animation: 1s gear-rotate linear infinite;
	-moz-animation: 1s gear-rotate linear infinite;
	animation: 1s gear-rotate linear infinite;
}
.gear-rotate-left{
  margin-top: -2.2em;
  margin-left: -.7em;
  top: 55%;
  width: 2em;
	height: 2em;
	background: #E9E581;
	position: absolute;
	border-radius: 1em;
  z-index: -1;
  -webkit-animation: 1s gear-rotate-left linear infinite;
  -moz-animation: 1s gear-rotate-left linear infinite;
  animation: 1s gear-rotate-left linear infinite;
}
.gear-rotate::before, .gear-rotate-left::before {
	width: 2.8em;
	height: 2.8em;
	background: 
    -webkit-linear-gradient(0deg,transparent 39%,#E9E581 39%,#E9E581 61%, transparent 61%),
    -webkit-linear-gradient(60deg,transparent 42%,#E9E581 42%,#E9E581 58%, transparent 58%),
    -webkit-linear-gradient(120deg,transparent 42%,#E9E581 42%,#E9E581 58%, transparent 58%);
	background: 
    -moz-linear-gradient(0deg,transparent 39%,#E9E581 39%,#47EC19 61%, transparent 61%),
    -moz-linear-gradient(60deg,transparent 42%,#E9E581 42%,#E9E581 58%, transparent 58%),
    -moz-linear-gradient(120deg,transparent 42%,#E9E581 42%,#E9E581 58%, transparent 58%);
	background: 
    -o-linear-gradient(0deg,transparent 39%,#E9E581 39%,#E9E581 61%, transparent 61%),
    -o-linear-gradient(60deg,transparent 42%,#E9E581 42%,#E9E581 58%, transparent 58%),
    -o-linear-gradient(120deg,transparent 42%,#47EC19 42%,#E9E581 58%, transparent 58%);
	background: -ms-linear-gradient(0deg,transparent 39%,#E9E581 39%,#E9E581 61%, transparent 61%),-ms-linear-gradient(60deg,transparent 42%,#E9E581 42%,#E9E581 58%, transparent 58%),-ms-linear-gradient(120deg,transparent 42%,#E9E581 42%,#E9E581 58%, transparent 58%);
	background: 
      linear-gradient(0deg,transparent 39%,#E9E581 39%,#E9E581 61%, transparent 61%),
    linear-gradient(60deg,transparent 42%,#E9E581 42%,#E9E581 58%, transparent 58%),
    linear-gradient(120deg,transparent 42%,#E9E581 42%,#E9E581 58%, transparent 58%);
	position: absolute;
	content:"";
	top: -.4em;
	left: -.4em;
	border-radius:1.4em;
}
.gear-rotate::after, .gear-rotate-left::after {
	width: 1em;
	height: 1em;
	background: #2B2B2B;
	position: absolute;
	content:"";
	top: .5em;
	left: .5em;
	border-radius: .5em;
}
/*
 * Keyframe Animations 
 */ 
@-webkit-keyframes gear-rotate {
  0% { 
    -webkit-transform: rotate(0deg);
  }
  100% { 
    -webkit-transform: rotate(-180deg); 
  }
}
@-moz-keyframes gear-rotate {
  0% { 
    transform: rotate(0deg);
  }
  100% { 
    transform: rotate(-180deg); 
  }
}
@keyframes gear-rotate {
  0% { 
    transform: rotate(0deg); 
  }
  100% { 
    transform: rotate(-180deg); 
  }
}
@-webkit-keyframes gear-rotate-left {
 0% {
   -webkit-transform: rotate(30deg); 
  }
  100% {
    -webkit-transform: rotate(210deg);
  }
}
@-moz-keyframes gear-rotate-left {
 0% { 
   -webkit-transform: rotate(30deg); 
  }
  100% { 
    -webkit-transform: rotate(210deg);
  }
}
@keyframes gear-rotate-left {
 0% { 
   -webkit-transform: rotate(30deg); 
  }
  100% { 
    -webkit-transform: rotate(210deg);
  }
}
.flex-container{
  display:flex;
  align-items: center;
  justify-content: left;
}
.Sn{
  position: absolute;
  top: 0;
  left: 10px;
  font-size: 1.9em;
  -webkit-text-stroke: 2px rgb(162, 162, 162); /* width and color */
  font-family: "Braah One", serif;
  color: rgb(255, 255, 255)
}
</style>
<div class="flex-container">
  <div class="gears-container">
    <div class="gear-rotate"></div>
    <div class="gear-rotate-left"></div>
    <div class="Sn" >Sn 50</div>
  </div>
  <h1 class = "rubik-mono-one-regular" style = "font-size: 40px">
  TinWidgets
  </h1>
</div>
TinWidgets is a project focused on creating customizable and animated widgets for web applications. The widgets are designed to be visually appealing and easy to integrate into any web project.

### Features

- Customizable gears animation
- Multiple font styles
- Responsive design
- Easy to integrate

### Installation

To install TinWidgets, you can clone the repository:

```bash
git clone https://github.com/zar-hub/tinwidgets.git
```

### Usage

Include the provided CSS and HTML in your project to start using TinWidgets. Customize the styles as needed to fit your design.

### Contributing

Contributions are welcome! Please fork the repository and submit a pull request with your changes.
The library comes with a logger, there are two ways to get the logger messages:
read from the ```debug.log``` file with the following command:
```bash
tail -f debug.log
```
or to use the output widget that comes with the library executing this command in a cell:
```python
tinw.widget_handler.show_logs()
```


### License

This project is licensed under the MIT License.

### Contact

For any questions or suggestions, please open an issue or contact the project maintainer at your.email@example.com.



