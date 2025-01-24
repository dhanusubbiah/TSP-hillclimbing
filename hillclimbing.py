import random
import ast
import streamlit as st
import mysql.connector
from mysql.connector import Error

def randomsolution(distance):
    cities = list(range(len(distance)))
    solution = random.sample(cities, len(cities))
    return solution

def route_length(w, solution):
    route_length = 0
    n = len(solution)
    for i in range(n - 1):
        route_length += w[solution[i]][solution[i + 1]]
    return route_length

def get_neighbours(solution):
    neighbours = []
    n = len(solution)
    for i in range(n):
        for j in range(i + 1, n):
            neighbour = solution.copy()
            neighbour[i], neighbour[j] = neighbour[j], neighbour[i]
            neighbours.append(neighbour)
    return neighbours

def get_best_neighbours(w, neighbours):
    best_route_length = route_length(w, neighbours[0])
    best_neighbour = neighbours[0]
    for neighbour in neighbours:
        current_route_length = route_length(w, neighbour)
        if current_route_length < best_route_length:
            best_route_length = current_route_length
            best_neighbour = neighbour
    return best_neighbour, best_route_length

def hill_climbing(w, initial_solution, max_iterations=1000):
    current_solution = initial_solution
    current_length = route_length(w, current_solution)
    for i in range(max_iterations):
        neighbours = get_neighbours(current_solution)
        best_neighbour, best_length = get_best_neighbours(w, neighbours)
        if best_length < current_length:
            current_solution = best_neighbour
            current_length = best_length
        else:
            break
    return current_solution,current_length

def save_to_mysql(solution, length):
    connection=None
    try:
        connection = mysql.connector.connect(
            host='localhost',
            user='root',
            password='dhanushree$250406',  
            database='hillclimbing'
        )

        if connection.is_connected():
            cursor = connection.cursor()

            create_table_query = '''
            CREATE TABLE IF NOT EXISTS hill_climbing_results (
                id INT AUTO_INCREMENT PRIMARY KEY,
                solution TEXT NOT NULL,
                route_length FLOAT NOT NULL
            );
            '''
            cursor.execute(create_table_query)

            insert_query = '''
            INSERT INTO hill_climbing_results (solution, route_length)
            VALUES (%s, %s);
            '''
            cursor.execute(insert_query, (str(solution), length))

            connection.commit()
            st.success("Data successfully inserted into the MySQL database.")

    except Error as e:
        st.error(f"Error while connecting to MySQL: {e}")

    finally:
        if connection and connection.is_connected():
            cursor.close()
            connection.close()
def main():
   
    
    background_image_url = "https://images.unsplash.com/photo-1736843640230-ea1e8241ae42?w=500&auto=format&fit=crop&q=60&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHx0b3BpYy1mZWVkfDE5fGJvOGpRS1RhRTBZfHxlbnwwfHx8fHw%3D"
    st.markdown(
        f"""
        <style>
            .stApp {{
                background-image: url('{background_image_url}');
                background-size: cover;
                background-position: center;
            }}
        </style>
        """, 
        unsafe_allow_html=True
    )

    st.title("TRAVELLING SALES PERSON - HILL CLIMBING ALGORITHM!!!")

    w = st.text_input("Enter the distance matrix: Eg: [[0,1,2],[1,0,3]...]")

    global solution, length
    solution=None
    length=None
    

    if st.button("Generate Random Solution"):
        try:
            distance = ast.literal_eval(w)
            solution = randomsolution(distance)
            length = route_length(distance, solution)
            st.write(f"**Random Solution:** {solution}")
            st.write(f"**Route Length:** {length}")
        except Exception as e:
            st.write("Invalid input. Please enter a valid distance matrix.")

    if st.button("Run hill climbing"):
        try:
            distance = ast.literal_eval(w)
            initial_solution = randomsolution(distance)
            st.write(f"**Initial Random Solution:** {initial_solution}")
            st.write(f"**Initial Route Length:** {route_length(distance, initial_solution)}")

            solution,length = hill_climbing(distance, initial_solution)
            st.write(f"**Best Solution after Hill Climbing:** {solution}")
            st.write(f"**Best Route Length:** {length}")
        except Exception as e:
            st.write("Invalid input. Please enter a valid distance matrix.")

    
    if st.button("Export to MySQL Database"):
        try:
            distance = ast.literal_eval(w)
            initial_solution = randomsolution(distance)
            solution,length=hill_climbing(distance,initial_solution)
            if solution is not None and length is not None:
                save_to_mysql(solution,length)
                st.write("Data successfully exported to MySQL database.")
            else:
                st.write("Please run the hill climbing algorithm first.")
        except Exception as e:
            st.write(f"An error occurred during database export: {e}")

if __name__ == "__main__":
    main()



