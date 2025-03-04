import sympy as sp
import streamlit as st

# Hard-coded unit conversion function
unit_conversions = {
    "meters": ["feet"],
    "feet": ["meters"],
    "kilograms": ["pounds"],
    "pounds": ["kilograms"],
    "Celsius": ["Fahrenheit"],
    "Fahrenheit": ["Celsius"],
    "joules": ["calories"],
    "calories": ["joules"],
    "liters": ["gallons"],
    "gallons": ["liters"],
    "newtons": ["dynes"],
    "dynes": ["newtons"],
    "watts": ["horsepower"],
    "horsepower": ["watts"],
    "km/h": ["m/s"],
    "m/s": ["km/h"],
    "bar": ["pascal"],
    "pascal": ["bar", "atm"],
    "atm": ["pascal"]
}

def convert_units(value, from_unit, to_unit):
    conversions = {
        "meters to feet": 3.28084,
        "feet to meters": 0.3048,
        "kilograms to pounds": 2.20462,
        "pounds to kilograms": 0.453592,
        "Celsius to Fahrenheit": lambda c: (c * 9/5) + 32,
        "Fahrenheit to Celsius": lambda f: (f - 32) * 5/9,
        "joules to calories": 0.239006,
        "calories to joules": 4.184,
        "liters to gallons": 0.264172,
        "gallons to liters": 3.78541,
        "newtons to dynes": 100000,
        "dynes to newtons": 0.00001,
        "watts to horsepower": 0.00134102,
        "horsepower to watts": 745.7,
        "km/h to m/s": 0.277778,
        "m/s to km/h": 3.6,
        "bar to pascal": 100000,
        "pascal to bar": 0.00001,
        "atm to pascal": 101325,
        "pascal to atm": 0.000009869,
    }
    
    key = f"{from_unit} to {to_unit}"
    if key in conversions:
        conversion = conversions[key]
        return conversion(value) if callable(conversion) else value * conversion
    else:
        return "Conversion not available"

# Streamlit UI
st.title("Smart Formula Solver & Unit Converter ")

st.header("Unit Converter")
value = st.number_input("Enter value", min_value=0.0, format="%.6f")

unit_options = list(unit_conversions.keys())
from_unit = st.selectbox("From unit", ["Select"] + unit_options)

# Show only available conversions based on selected "From unit"
to_unit_options = unit_conversions.get(from_unit, [])
to_unit = st.selectbox("To unit", ["Select"] + to_unit_options)

if st.button("Convert"):
    if from_unit == "Select" or to_unit == "Select":
        st.error("Please select valid units.")
    else:
        conversion_result = convert_units(value, from_unit, to_unit)
        st.write("Conversion Result:", conversion_result)




# Define all physics formulas
formulas = {
    "Newton's Second Law (F = ma)": sp.Eq(sp.Symbol('F'), sp.Symbol('m') * sp.Symbol('a')),
    "Kinetic Energy (KE = 1/2 mv²)": sp.Eq(sp.Symbol('KE'), (1/2) * sp.Symbol('m') * sp.Symbol('v')**2),
    "Momentum (p = mv)": sp.Eq(sp.Symbol('p'), sp.Symbol('m') * sp.Symbol('v')),
    "Work Done (W = Fd)": sp.Eq(sp.Symbol('W'), sp.Symbol('F') * sp.Symbol('d')),
    "Power (P = W/t)": sp.Eq(sp.Symbol('P'), sp.Symbol('W') / sp.Symbol('t')),
    "Ohm's Law (V = IR)": sp.Eq(sp.Symbol('V'), sp.Symbol('I') * sp.Symbol('R')),
    "Electric Power (P = VI)": sp.Eq(sp.Symbol('P'), sp.Symbol('V') * sp.Symbol('I')),
    "Gravitational Force (Fg = Gm₁m₂/r²)": sp.Eq(sp.Symbol('Fg'), sp.Symbol('G') * sp.Symbol('m1') * sp.Symbol('m2') / sp.Symbol('r')**2),
    "Ideal Gas Law (PV = nRT)": sp.Eq(sp.Symbol('PV'), sp.Symbol('n') * sp.Symbol('R') * sp.Symbol('T')),
    "Einstein's Energy (E = mc²)": sp.Eq(sp.Symbol('E'), sp.Symbol('m') * sp.Symbol('c')**2)
}

#  Function to solve equations
def solve_formula(formula_key, given_values):
    equation = formulas[formula_key]  # Select formula
    known_vars = {sp.Symbol(k): v for k, v in given_values.items()}  # Convert inputs to SymPy symbols
    missing_vars = list(equation.free_symbols - known_vars.keys())  # Find missing variables

    if len(missing_vars) == 1:
        solution = sp.solve(equation.subs(known_vars), missing_vars[0])
        return f"{missing_vars[0]} = {solution[0]}"
    else:
        return "Error: Please enter correct values!"

#  Streamlit UI
st.title("Physics Formula Solver")
st.write("Enter values and find missing variables!")

#  User selects a formula
selected_formula = st.selectbox("Choose a formula:", list(formulas.keys()))

#  Get user input dynamically
equation = formulas[selected_formula]
symbols_in_equation = [str(sym) for sym in equation.free_symbols]

given_values = {}
for symbol in symbols_in_equation:
    value = st.text_input(f"Enter {symbol} (leave blank if unknown):")
    if value:
        given_values[symbol] = float(value)

#  Solve button
if st.button("Solve"):
    result = solve_formula(selected_formula, given_values)
    st.success(result)
