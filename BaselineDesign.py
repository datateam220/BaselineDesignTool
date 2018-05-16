print('Loading Dependencies...')
from tkinter import *
from tkinter import ttk
import tkFileDialog, arcpy, os
from Baseline_Design_Package import Controller as Controller
print('Configuring GUI...')
#turn off edit logging, speeds up edits greatly
arcpy.SetLogHistory(False)


def scrub(*args):
	#updates the scrubbed value
	value = scrubbedvar.get()
	scrubbedvar.set(value)

def define_workspace():
	#defines the workspace that the analysis will take place in
	change_lbl(workspacevar,'')
	folder_name = tkFileDialog.askdirectory()
	change_lbl(workspacevar,folder_name)
	print('Loading selected GDB...')
	generate_fcs(folder_name)

def change_lbl(labelvar,label):
	#changes a label variable
	labelvar.set(label)

def generate_fcs(workspace):
	#generate a list of feature classes after defining the workspace
	try:
		#check if the foler may actually be a GDB. This is a pretty weak check as
		#folders can end in .gdb but are not actually GDBs. hopefully, attempting
		#to do some of the following operations on an invalid folder will throw 
		#an error to trigger the except clause.
		if '.gdb' not in workspace:
			raise ValueError('Not a valid workspace.')
		arcpy.env.workspace = workspace
		fcs = []
		for fds in arcpy.ListDatasets('','feature') + ['']:
			for fc in arcpy.ListFeatureClasses('','',fds):
				fcs.append(os.path.join(fds, fc))
		
		fcvar.set("")
		fcscb['values'] = fcs
		fcscb['state'] = "readonly"
	except:
		change_lbl(workspacevar,'INVALID WORKSPACE')
		print('Invalid GDB selected...')
		fcscb['values'] = []
		fcscb['state'] = "disabled"
		fcvar.set('')

def set_fc(*args):
	value = fcvar.get()
	fcvar.set(value)

def fc_loading(*args):
	fcvar.set('Loading GDB...')

def set_manufacturer(*args):
	value = manufacturervar.get()
	manufacturervar.set(value)

def set_processing(*args):
	if design_applied.get() == 0:
		statusvar.set("Processing Baseline Design - Do not press anything.")
		startButton['state'] = 'disabled'
	else:
		startButton['state'] = 'disabled'
		statusvar.set("BASELINE DESIGN APPLIED SUCCESSFULLY!")

def start_analysis(*args):
	#mainframe.after(1,set_processing)
	print("Processing Baseline Design - Do not press anything.")
	try:	
		if not design_applied.get() == 1:	
			fields = ['TANKO_ID','FIXTURTYPE','LAMPTYPE','STREETDESN','ARM_DIR','OTHERWATT','DESWATT','DESDIST', 'DESSTAT']
			def check_scrubbed_param(fields):
				if scrubbedvar.get() == 'Yes':
					fields.append('DESOLDWATT')
					return fields
				elif scrubbedvar.get() == 'No':
					fields.append('OLDWATT')
					return fields
				else:
					print('Scrubbed Variable must be set')
			def check_DESSTAT():
				Fields = [field.name for field in arcpy.ListFields(fcvar.get())]
				if 'DESSTAT' not in Fields:
					print('DESSTAT is not a field in this feature class, adding it now.')
					arcpy.AddField_management(fcvar.get(), 'DESSTAT', 'TEXT',field_length = 100)
					print('DESSTAT added to feature class.')
				#Check if DESWATT and DESDIST are fields. Throw error if not to alert the user to add/populate them
				if 'DESWATT' not in Fields:
					raise Exception('DESWATT is not a field in the dataset. Add it and populate it before running this script')
				elif 'DESDIST' not in Fields:
					raise Exception('DESDIST is not a field in the dataset. Add it and populate it before running this script')
				else:
					print('Workspace initialized.')
			check_DESSTAT()
			fields = check_scrubbed_param(fields)
			Analysis = Controller.DataHandler(fcvar.get(), fields, manufacturervar.get())
			Analysis.apply_design()
			statusvar.set("Baseline design applied successfully")
			design_applied.set(1)
		else:
			statusvar.set("You clicked more than once, didn't you?")
	except Exception as e:
		raise
		statusvar.set("ERROR PROCESSING BASELINE DESIGN")
	
root = Tk()
root.title("Baseline Design Tool")

mainframe = ttk.Frame(root, padding="25 25 25 25")
mainframe.grid(column=0, row=0, sticky=(N, W, E, S))
mainframe.columnconfigure(0, weight=1)
mainframe.rowconfigure(0, weight=1)

workspacevar = StringVar()
fcvar = StringVar()
scrubbedvar = StringVar()
manufacturervar = StringVar()
scrubbedvar.set('No')
statusvar = StringVar()
design_applied = BooleanVar()
design_applied.set(0)

#labels
ttk.Label(mainframe, text = "Select GDB:").grid(column =1, row = 1, sticky = W)
ttk.Label(mainframe, text = "Select Feature Class:").grid(column = 1, row = 2, sticky = W)
ttk.Label(mainframe, text = "Dataset Scrubbed:").grid(column =1, row = 3, sticky = W)
ttk.Label(mainframe, text = "Select Manufacturer:").grid(column =1, row = 4, sticky = W)

#widgets set up
# - Select GDB
workspaceButton = ttk.Button(mainframe,text = "Browse for GDB", command = define_workspace)
workspaceButton.grid(column = 2, row = 1, sticky = (W, E))
ttk.Label(mainframe,textvariable = workspacevar).grid(column = 3, row = 1, sticky = E)
workspaceButton.bind('<ButtonRelease>',fc_loading)

#- Select Feature Class
fcscb = ttk.Combobox(mainframe,state = "disabled",textvariable=fcvar)
fcscb.grid(column = 2, row = 2, sticky = (E,W))
fcscb.bind('<<ComboboxSelected>>',set_fc)
ttk.Label(mainframe,textvariable = fcvar).grid(column =3, row =2, sticky = E)

# - Scrubbed
scrubbed = ttk.Combobox(mainframe,state="readonly", textvariable=scrubbedvar)
scrubbed.grid(column = 2, row = 3, sticky = (W, E))
scrubbed['values'] = ['Yes','No']
scrubbed.bind('<<ComboboxSelected>>', scrub)

# - Manufacturer
manufacturer = ttk.Combobox(mainframe,state="readonly", textvariable=manufacturervar)
manufacturer.grid(column = 2, row = 4, sticky = (W, E))
manufacturer['values'] = ['Brand Neutral']
manufacturer.bind('<<ComboboxSelected>>', set_manufacturer)

# - Start Analysis
startButton = ttk.Button(mainframe,text = "Apply Baseline Design", command = start_analysis)
startButton.grid(column = 2, row = 6, sticky = (E,W))
ttk.Label(mainframe,textvariable = statusvar, foreground = 'red').grid(column = 2, row = 7, sticky= (E,W), columnspan = 3)
startButton.bind('<ButtonPress>',set_processing)
startButton.bind('<ButtonRelease>', start_analysis)


for child in mainframe.winfo_children(): child.grid_configure(padx=10, pady=10)

#root.bind('<Return>', start_analysis)

root.mainloop()