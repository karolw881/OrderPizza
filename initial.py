import clips
import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
from tkinter import scrolledtext
from PIL import Image, ImageTk

# Initialize CLIPS environment
env = clips.Environment()
env.load('fact3.clp')
env.reset()
