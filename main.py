import threading
from kivymd.app import MDApp
from kivymd.uix.boxlayout import MDBoxLayout
from kivy.uix.widget import Widget
from kivymd.uix.gridlayout import MDGridLayout
from kivymd.uix.button import MDRoundFlatButton,MDRaisedButton
from kivy.clock import Clock
from kivymd.uix.dialog import MDDialog
from kivy.properties import StringProperty,BooleanProperty
from kivy.uix.label import Label
from collections import OrderedDict
from kivymd.uix.scrollview import MDScrollView
from kivymd.uix.screen import MDScreen
import matplotlib.pyplot as plt
from simplex import simplex_solver
from kivymd.uix.textfield import MDTextFieldRect
from kivymd.uix.label import MDLabel
from kivymd.uix.screenmanager import MDScreenManager
import pulp_pack as lp
from solver import optimal_finder
from kivymd.uix.screen import MDScreen
from kivymd.uix.card import MDCard
from kivymd.uix.spinner import MDSpinner
from garden_matplotlib.backend_kivyagg import FigureCanvasKivyAgg
from kivymd.uix.datatables import MDDataTable
from kivymd.uix.dropdownitem import MDDropDownItem
from kivy.metrics import dp
from kivymd.uix.transition import MDFadeSlideTransition
from kivy.uix.spinner import Spinner, SpinnerOption
from kivy.uix.dropdown import DropDown
from kivy.utils import get_color_from_hex
from kivymd.uix.toolbar import MDTopAppBar,MDBottomAppBar
import logging
from test_graphical import graphical_method_plotter
from kivy.config import Config
from kivy.lang import Builder
import matplotlib
matplotlib.use('Agg')
matplotlib.pyplot.set_loglevel(level = 'debug')
logging.getLogger('matplotlib').setLevel(logging.ERROR)
logging.getLogger('kivy.garden.matplotlib').setLevel(logging.WARNING)
logging.getLogger('PIL').setLevel(logging.WARNING)
Config.set('input', 'mtdev_%(name)s', 'probesysfs,provider=mtdev')
sm = MDScreenManager(transition=MDFadeSlideTransition())
logging.info("This is a start message")
class SpinnerOptions(SpinnerOption):
    def __init__(self, **kwargs):
        super(SpinnerOptions, self).__init__(**kwargs)
        self.background_normal = ''
        self.background_color = (1, 1, 1, 1)
        self.height = dp(26)
        self.font_size = dp(16)
        self.color = get_color_from_hex('#800080') 

class SpinnerDropdown(DropDown):
    def __init__(self, **kwargs):
        super(SpinnerDropdown, self).__init__(**kwargs)
        self.auto_width = False
        self.width = 150

class SpinnerWidget(Spinner):
    def __init__(self, **kwargs):
        super(SpinnerWidget, self).__init__(**kwargs)
        self.dropdown_cls = SpinnerDropdown
        self.option_cls = SpinnerOptions
        
class FirstScreen(MDScreen):
    
    def on_text(self, text):
        try:
            input_number = int(text)
            # Input is valid
            if input_number<2 or input_number>4:
                self.ids.var_num.helper_text = "Enter value from 2 to 4"
                self.ids.var_num.error = True
            else:
                self.ids.var_num.helper_text = ""
                self.ids.var_num.error = False
                print("Valid input:", input_number)

        except ValueError:
            # Input is invalid
            self.ids.var_num.helper_text = "Enter value from 2 to 4"
            self.ids.var_num.error = True
    def on_text1(self, text):
        try:
            input_number = int(text)
            if input_number<2 or input_number>4:
                self.ids.const_num.helper_text = "Enter value from 2 to 4"
                self.ids.const_num.error = True
            else:
                self.ids.const_num.helper_text = ""
                self.ids.const_num.error = False
                print("Valid input:", input_number)

        except ValueError:
            # Input is invalid
            self.ids.const_num.helper_text = "Enter value from 2 to 4"
            self.ids.const_num.error = True
    def changer_next(self):
        text_input1 = self.ids.var_num
        text_input2 = self.ids.const_num
        if text_input1.error or text_input2.error:
            dialog = MDDialog(title="Invalid Input",
                              text="Please enter a valid number.",
                              size_hint=(0.8, None),
                              buttons=[MDRaisedButton(text="Close",on_release=lambda _:dialog.dismiss())])
            dialog.open()
        elif text_input1.text == "" or text_input2.text == "":
            dialog = MDDialog(title="Invalid Input",
                              text="Please enter a valid number.",
                              size_hint=(0.8, None),
                              buttons=[MDRaisedButton(text="Close",on_release=lambda _:dialog.dismiss())])
            dialog.open()
        else:
            sm.get_screen('Second').start()
class SecondScreen(MDScreen):
    text_inputs = OrderedDict()
    rhs_inputs = {}
    inequal_inputs = {}
    obj_inputs = {}
    def start(self):
        sm.current='Second'
        var_num = int(sm.get_screen('First').ids.var_num.text)
        const_num = int(sm.get_screen('First').ids.const_num.text)
        first_box = MDBoxLayout(size=self.size,orientation="vertical")
        self.add_widget(first_box)
        md=MDCard(size_hint=(1, 1),
        pos_hint={"center_x": 0.5, "center_y": 0.5},
        spacing=dp(25),
        orientation='vertical',
        radius=[dp(30)])
        
        obj_grid = MDGridLayout(cols=3*var_num,size_hint=(1,None),height=dp(30))
        value = MDGridLayout(cols=var_num,size_hint=(1,None),height=dp(30))
        top_bar = MDTopAppBar(title="Enter Objective Function And Constraints Coefficients ")
        top_bar.left_action_items =[["arrow-left",lambda x:self.changer_prev()]]
        first_box.add_widget(top_bar)
        first_box.add_widget(obj_grid)
        first_box.add_widget(md)
        max_min =SpinnerWidget(text='Max',values = ('Max','Min'),
                               font_size=dp(18),
                               background_color=(0, 0, 0, 0),
                               color=get_color_from_hex('#800080'))
        self.obj_inputs['Max']=max_min
        obj_grid.add_widget(max_min)
        for obj in range(var_num):
            obj_co = MDTextFieldRect(size_hint=(None,None),
                                                width=dp(30),height=dp(30),
                                                font_size=dp(16))
            obj_grid.add_widget(obj_co)
            expression = f'x{obj+1}'  # Create the mathematical expression x[obj+1]
            obj_grid.add_widget(Label(text =expression,
                                        markup=True,
                                        color=(0,0,0,1),
                                        font_size=dp(20),font_name='BrandonGrotesque-Black'))
            if obj < var_num-1:
                obj_grid.add_widget(Label(text='+',color=(0,0,0,1),font_size=dp(18)))
            self.obj_inputs[f'co_{obj+1}']=obj_co
        
        box = MDBoxLayout(orientation="vertical",spacing=dp(40))
        
        less_than_or_equal_to = u'\u2264'
        for j in range(const_num):  # Add TextInputs for constraints
            index = 1
            grid = MDGridLayout(cols=3*var_num+1,size_hint=(1,None),height=dp(30))
            for i in range(var_num):  # One additional column for the constraint coefficients
                constraint_input = MDTextFieldRect(size_hint=(None,None),width=dp(30),height=dp(30),font_size=dp(16))
                grid.add_widget(constraint_input)
                expression = f'x{index}'  # Create the mathematical expression x[obj+1]
                grid.add_widget(Label(text =expression,
                                        markup=True,
                                        color=(0,0,0,1),
                                        font_size=dp(20),font_name='BrandonGrotesque-Black'))
                if i < var_num-1:
                    grid.add_widget(MDLabel(text='+',color=(0,0,0,1),font_size=dp(28),halign='center'))
                self.text_inputs[f'constraint_{j+1}_{i+1}'] = constraint_input
                index+=1
            inequal = SpinnerWidget(text=less_than_or_equal_to,
                                    values=(less_than_or_equal_to, '≥'), font_size=dp(30), background_color=(0, 0, 0, 0),color=(0,0,0,1))
            
            inp = MDTextFieldRect(size_hint=(None,None),width=dp(30),height=dp(30),font_size=dp(16))
            self.rhs_inputs[f'rhs_{j+1}']=inp
            
            self.inequal_inputs[f'inequal_{j+1}'] = inequal
            grid.add_widget(inequal)
            grid.add_widget(inp)
            box.add_widget(grid)
        md.add_widget(box)
        md.add_widget(Widget(size_hint_y=None,height=dp(-(50*const_num )+ 300)))
        graphical_method = MDRoundFlatButton(text="Graphial Method",
            font_size=dp(20),
            size_hint=(.5,None),
            pos_hint={"center_x": 0.5})
        md.add_widget(graphical_method)
        simplex_method = MDRoundFlatButton(text="Simplex Method",
            font_size=dp(20),
            size_hint=(.5,None),
            pos_hint={"center_x": 0.5})
        md.add_widget(simplex_method)
        graphical_method.bind(on_press=self.changer_next)
        simplex_method.bind(on_press=self.changer_simplex)
    def changer_prev(self,*args):
        sm.current = "First"
        self.clear_widgets()
        self.text_inputs = OrderedDict()
        self.rhs_inputs = {}
        self.inequal_inputs = {}
        self.obj_inputs = {}
    def changer_next(self,*args):
        l = list(self.text_inputs.values())
        l.extend(list(self.obj_inputs.values())[1:])
        
        if "" in [i.text.strip() for i in l]:
            dialog = MDDialog(title="Invalid Input",
                              text="Please make sure all boxes are filled",
                              size_hint=(0.8, None),
                              buttons=[MDRaisedButton(text="Close",on_release=lambda _:dialog.dismiss())])
            dialog.open()
        elif int(sm.get_screen('First').ids.var_num.text) > 2:
            dialog = MDDialog(title="Invalid Input",
                              text="Graphical method works for only two variables",
                              size_hint=(0.8, None),
                              buttons=[MDRaisedButton(text="Close",on_release=lambda _:dialog.dismiss())])
            dialog.open()
        else:
            try:
                v=[eval(i.text) for i in l]
                sm.get_screen("Third").start()
            except:
                dialog = MDDialog(title="Invalid Input",
                              text="Enter Valid Input",
                              size_hint=(0.8, None),
                              buttons=[MDRaisedButton(text="Close",on_release=lambda _:dialog.dismiss())])
                dialog.open()
            
    def changer_simplex(self,*args):
        l = list(self.text_inputs.values())
        l.extend(list(self.obj_inputs.values())[1:])
        
        if "" in [i.text.strip() for i in l]:
            dialog = MDDialog(title="Invalid Input",
                              text="Please make sure all boxes are filled",
                              size_hint=(0.8, None),
                              buttons=[MDRaisedButton(text="Close",on_release=lambda _:dialog.dismiss())])
            dialog.open()
        elif '≥' in [i.text for i in  list(self.inequal_inputs.values())]:
            dialog = MDDialog(title="Invalid Input",
                              text="Please Try Dual Simplex",
                              size_hint=(0.8, None),
                              buttons=[MDRaisedButton(text="Close",on_release=lambda _:dialog.dismiss())])
            dialog.open()
        else:
            try:
                v=[eval(i.text) for i in l]
                sm.get_screen("Fourth").start()
            except:
                dialog = MDDialog(title="Invalid Input",
                              text="Enter Valid Input",
                              size_hint=(0.8, None),
                              buttons=[MDRaisedButton(text="Close",on_release=lambda _:dialog.dismiss())])
                dialog.open()
            
class ThirdScreen(MDScreen):
    def start(self, *args):
        sm.current="Third"
        self.spinner = MDSpinner(size_hint=(None, None), size=(dp(46), dp(46)))
        self.spinner.pos_hint = {'center_x': 0.5, 'center_y': 0.5}
        self.add_widget(self.spinner)

        # Start a separate thread to run the graphical_method_plotter
        threading.Thread(target=self.run_graphical_method_plotter).start()

    def run_graphical_method_plotter(self):
        # Call graphical_method_plotter in the background thread
        graphical_method_plotter(int(sm.get_screen('First').ids.const_num.text),
                                 sm.get_screen('Second').text_inputs,
                                 sm.get_screen('Second').inequal_inputs,
                                 sm.get_screen('Second').rhs_inputs)

        # After the method is done, update the screen using Clock.schedule_once
        Clock.schedule_once(self.display_plot)
    def display_plot(self, dt):
        # Start the spinner by adding it to the screen
        self.remove_widget(self.spinner)
        '''
        ans,feasible = optimal_finder(int(sm.get_screen('First').ids.const_num.text),
                             sm.get_screen('Second').obj_inputs["Max"].text,
                             sm.get_screen('Second').obj_inputs,
                             sm.get_screen('Second').text_inputs,
                             sm.get_screen('Second').inequal_inputs,
                             sm.get_screen('Second').rhs_inputs)
        
        value = list(ans.values())
        if feasible.status == lp.LpStatusOptimal:
            self.lab =MDLabel(text = f"The optimal value of x1 is {value[0]} and that of x2 is {value[1]} with optimal objective value of {value[2]}",size_hint_x = 1,size_hint_y=.2)
        elif feasible.status == lp.LpStatusInfeasible:
            self.lab = MDLabel(text = "The problem is infeasible.",size_hint_x = 1,size_hint_y=.2)
        elif feasible.status == lp.LpStatusUnbounded:
            self.lab = MDLabel(text = "The problem is unbounded.",size_hint_x = 1,size_hint_y=.2)
        else:
            self.lab = MDLabel(text = "The problem has no solution.",size_hint_x = 1,size_hint_y=.2)
        '''
        self.first = MDBoxLayout(orientation="vertical",size=self.size)
        self.add_widget(self.first)
        top = MDTopAppBar(title="Plot")
        top.left_action_items = [["arrow-left",lambda x : self.prev()]]
        self.first.add_widget(top)
        self.first.add_widget(FigureCanvasKivyAgg(plt.gcf()))
        #self.first.add_widget(self.lab)
    def prev(self):
        sm.current = "Second"
        plt.clf()
        #self.first.remove_widget(self.lab)
class FourthScreen(MDScreen):
    def start(self, *args):
        sm.current ="Fourth"
        var_num =int(sm.get_screen('First').ids.var_num.text)
        const_num =int(sm.get_screen('First').ids.const_num.text)
        constraint_list = [eval(i.text) for i in list(sm.get_screen('Second').text_inputs.values())]
        max_min = list(sm.get_screen('Second').obj_inputs.values())[0].text
        if max_min == "Max":
            obj_list = [eval(i.text) for i in list(sm.get_screen('Second').obj_inputs.values())[1:]]
        else:
            obj_list = [-1*eval(i.text) for i in list(sm.get_screen('Second').obj_inputs.values())[1:]]
        rhs_list = [eval(i.text) for i in list(sm.get_screen('Second').rhs_inputs.values())]
        sol_dict,message = simplex_solver(constraint_list,obj_list,rhs_list,const_num,var_num)
        var_num =int(sm.get_screen('First').ids.var_num.text)
        const_num =int(sm.get_screen('First').ids.const_num.text)
        col_data = ["Basis"]
        col_data.extend([f'x{i}' for i in range(1,var_num+1)])
        col_data.extend([f'S{i}' for i in range(1,const_num+1)])
        col_data.append("RHS")
        
        basis_list = [i for i in list(sol_dict.values())[1::2]]
        basis_list= [[[item] for item in sublist] for sublist in basis_list]
        table_list = [i for i in list(sol_dict.values())[::2]]
        table_data = []
        for i in range(len(table_list)):
            table_data.append([item1 + item2 for item1, item2 in zip(basis_list[i], table_list[i])])
        flattened_list = [item for sublist in table_data for item in sublist]
        tableau_num = len(list(sol_dict.values()))//2
        sol_var = tuple(flattened_list[-1*i][0] for i in range(const_num+1,0,-1))
        ans = [eval(flattened_list[-1*i][-1]) for i in range(const_num+1,0,-1)]
        if max_min == "Max":
            ans[0]=-1*ans[0]
        else:
            pass
        ans1 = tuple(ans)
        if message == "Optimal Solution Found":
            solution = f"Optimum Solution exists and is given as  {sol_var} = {ans1}"
            self.lab = MDLabel(text=solution,size_hint=(1,.15))
        elif message == "Problem is unbounded":
            solution = f"{message}"
            self.lab = Label(text=solution,size_hint=(1,.15),font_name=BrandonGrotesque-Black)
        print(sol_var)
        self.data_table = MDDataTable(
            pos_hint = {'center_x': 0.5, 'center_y': 0.5},
            background_color_header="#5D3FD3",
            size_hint=(1,1),
            column_data = [[i,dp(55-8*var_num)] for i in col_data],
            row_data = flattened_list,
            use_pagination = True,
			rows_num = const_num+1,
			pagination_menu_height = dp(240),
			pagination_menu_pos = "auto",
        )
        self.ids.Box1.add_widget(self.data_table)
        self.ids.Box1.add_widget(self.lab)
    def prev(self):
        sm.current = "Second"
        self.ids.Box1.remove_widget(self.data_table)
        self.ids.Box1.remove_widget(self.lab)
class TestApp(MDApp):
    def build(self):
        self.theme_cls.theme_style = "Light"
        self.theme_cls.primary_palette = "DeepPurple"
        sm.add_widget(FirstScreen())
        sm.add_widget(SecondScreen())
        sm.add_widget(ThirdScreen())
        sm.add_widget(FourthScreen())
        Builder.load_file('test.kv')
        return sm
    def change_theme(self,value):
        if value:
            self.theme_cls.theme_style = "Dark"
        else:
            self.theme_cls.theme_style = "Light"

TestApp().run()
