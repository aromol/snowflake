import streamlit 
import pandas
import requests

import snowflake.connector
from urllib.error import URLError

#AÃ±adimos el titulo de nuestro sitio web

streamlit.title("Listado de comida")

streamlit.header('Breakfast Menu')
streamlit.text('ð¥£ Omega 3 & Blueberry Oatmeal')
streamlit.text('ð¥ Kale, Spinach & Rocket Smoothie')
streamlit.text('ð Hard-Boiled Free-Range Egg')
streamlit.text('ð¥ð Avocado toast')

streamlit.header('ðð¥­ Build Your Own Fruit Smoothie ð¥ð')

my_fruit_list = pandas.read_csv("https://uni-lab-files.s3.us-west-2.amazonaws.com/dabw/fruit_macros.txt")

# Display the table on the page.
my_fruit_list = my_fruit_list.set_index('Fruit')

# Let's put a pick list here so they can pick the fruit they want to include 
fruits_selected = streamlit.multiselect("Pick some fruits:", list(my_fruit_list.index),['Avocado', 'Strawberries'])
fruits_to_show = my_fruit_list.loc[fruits_selected]

streamlit.dataframe(fruits_to_show)

#Creacion de funcion
def get_fruityvice_data(this_fruit_choice):
  fruityvice_response = requests.get("https://fruityvice.com/api/fruit/"+fruit_choice)
  #streamlit.text(fruityvice_response.json())

  # write your own comment -what does the next line do? 
  fruityvice_normalized = pandas.json_normalize(fruityvice_response.json())
  return fruityvice_normalized
  
streamlit.header("Fruityvice Fruit Advice!")
try:
  fruit_choice = streamlit.text_input('What fruit would you like information about?')
  if not fruit_choice:
    streamlit.error('Please select a fruit to get information')
  else:
    back_from_function = get_fruityvice_data(fruit_choice)
    # write your own comment - what does this do?
    streamlit.dataframe(back_from_function)
except URLError as e:
  streamlit.error()

#streamlit.stop()
streamlit.header("The fruit load list contains:")
#Funcion de listado de datos desde snowflake
def get_fruit_load_list():
  with my_cnx.cursor() as my_cur:
    my_cur.execute("select * from fruit_load_list")
    return my_cur.fetchall()
  
if streamlit.button('Get Fruit Load List'):
  my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])
  my_data_rows = get_fruit_load_list()
  streamlit.dataframe(my_data_rows)

#funcion de insersion a Snowflake
def insert_row_snowflake(new_fruit):
  with my_cnx.cursor() as my_cur:
    query = "insert into fruit_load_list values ('from streamlit "+ new_fruit+"')"
    my_cur.execute(query)
    return "Tranks fro adding "+ new_fruit
  
add_my_fruit = streamlit.text_input('What fruit would you like to add?')
if streamlit.button('Add a Fruit to the List'):
  my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])
  back_from_function = insert_row_snowflake(add_my_fruit)
  streamlit.text(back_from_function)




