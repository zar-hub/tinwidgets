<div style="margin: 0px">
		<img src="media/header.svg" />
</div>

TinWidgets is a project focused on creating customizable and animated widgets for web applications. The widgets are designed to be visually appealing and easy to integrate into any web project.

### Features
- Interactive Matplotlib graphs
- Widgets support

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
### Dev
**Widget traitlets** traitlets are a Python framework for eventful variables interaction.
The basic concept is that a traitlet can be *observed*, and it's update triggers some callback function.
The python widget system uses this traitlets feature to handle the state, usually the traitlets of the widgets are called `variable` (duh).
There are some utilities in the [traitlet docs](https://www.google.com/search?client=firefox-b-d&q=zen+copy+url+shortcuop)
which are used to **link** two different traitles. 

### License

This project is licensed under the MIT License.