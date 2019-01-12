#!/usr/bin/env python3
"""
DeviceManagement Database module.
Contains all interactions between the webapp and the queries to the database.
"""

import configparser
import datetime
from typing import List, Optional

import setup_vendor_path  # noqa
import pg8000

################################################################################
#   Welcome to the database file, where all the query magic happens.
#   My biggest tip is look at the *week 9 lab*.
#   Important information:
#       - If you're getting issues and getting locked out of your database.
#           You may have reached the maximum number of connections.
#           Why? (You're not closing things!) Be careful!
#       - Check things *carefully*.
#       - There may be better ways to do things, this is just for example
#           purposes
#       - ORDERING MATTERS
#           - Unfortunately to make it easier for everyone, we have to ask that
#               your columns are in order. WATCH YOUR SELECTS!! :)
#   Good luck!
#       And remember to have some fun :D
################################################################################


#####################################################
#   Database Connect
#   (No need to touch
#       (unless the exception is potatoing))
#####################################################

def database_connect():
    """
    Connects to the database using the connection string.
    If 'None' was returned it means there was an issue connecting to
    the database. It would be wise to handle this ;)
    """
    # Read the config file
    config = configparser.ConfigParser()
    config.read('config.ini')
    if 'database' not in config['DATABASE']:
        config['DATABASE']['database'] = config['DATABASE']['user']

    # Create a connection to the database
    connection = None
    try:
        # Parses the config file and connects using the connect string
        connection = pg8000.connect(database=config['DATABASE']['database'],
                                    user=config['DATABASE']['user'],
                                    password=config['DATABASE']['password'],
                                    host=config['DATABASE']['host'])
    except pg8000.OperationalError as operation_error:
        print("""Error, you haven't updated your config.ini or you have a bad
        connection, please try again. (Update your files first, then check
        internet connection)
        """)
        print(operation_error)
        return None

    # return the connection to use
    return connection


#####################################################
#   Query (a + a[i])
#   Login
#####################################################

def check_login(employee_id, password: str) -> Optional[dict]:
    """
    Check that the users information exists in the database.
        - True => return the user data
        - False => return None
    """

    # Note: this example system is not well-designed for security.
    # There are several serious problems. One is that the database
    # stores passwords directly; a better design would "salt" each password
    # and then hash the result, and store only the hash.
    # This is ok for a toy assignment, but do not use this code as a model when you are
    # writing a real system for a client or yourself.

    # TODO
    # Check if the user details are correct!
    # Return the relevant information (watch the order!)

    # TODO Dummy data - change rows to be useful!
    # NOTE: Make sure you take care of ORDER!!!

    # employee_info = [
    #     1337,                       # empid
    #     'Porter Tato Head',         # name
    #     '123 Fake Street',          # homeAddress
    #     datetime.date(1970, 1, 1),  # dateOfBirth
    # ]

    # user = {
    #     'empid': employee_info[0],
    #     'name': employee_info[1],
    #     'homeAddress': employee_info[2],
    #     'dateOfBirth': employee_info[3],
    # }

    connection = database_connect();

    if(connection is None):
        print("check_login: The connection is fail!");
        return None;

    cursor = connection.cursor()

    try:
        # cursor.execute("SELECT * FROM student WHERE sid=%s", (sid))

        query = '''SELECT name, homeAddress, dateOfBirth
                    FROM Employee
                    WHERE empID = %s AND password = %s;''';

        cursor.execute(query, (employee_id, password));
        results = cursor.fetchone();
        cursor.close() # IMPORTANT: close cursor
        connection.close() # IMPORTANT: close connection
        if(results is None):
            # What happens when results is NULL?
            return None;

    except Exception as e:
        # This happens if there is an error executing the query
        print("Error executing function");
        print(e);
        cursor.close();                    # Close the cursor
        connection.close();

    user = {
        'empid': employee_id,
        'name': results[0],
        'homeAddress': results[1],
        'dateOfBirth': results[2]
    }

    return user


#####################################################
#   Query (f[i])
#   Is Manager?
#####################################################

def is_manager(employee_id: int) -> Optional[str]:
    """
    Get the department the employee is a manager of, if any.
    Returns None if the employee doesn't manage a department.
    """

    # TODO Dummy Data - Change to be useful!
    # manager_of = 'RND'

    # return manager_of

    connection = database_connect();

    if(connection is None):
        print("is_manager: The connection is fail!");
        return None;

    cursor = connection.cursor();

    try:
        # cursor.execute("SELECT * FROM student WHERE sid=%s", (sid))

        query = '''SELECT name
                    FROM Department
                    WHERE manager = %s;''';

        cursor.execute(query, (employee_id,));
        manage_department = cursor.fetchall();
        # print(manage_department);

        cursor.close() # IMPORTANT: close cursor
        connection.close() # IMPORTANT: close connection


    except Exception as e:
        # This happens if there is an error executing the query
        print("Error executing function");
        print(e);
        cursor.close();                    # Close the cursor
        connection.close();

    if(len(manage_department) == 0):
        return None;

    return manage_department[0][0];


#####################################################
#   Query (a[ii])
#   Get My Used Devices
#####################################################

def get_devices_used_by(employee_id: int) -> list:
    """
    Get a list of all the devices used by the employee.
    """

    # TODO Dummy Data - Change to be useful!
    # Return a list of devices issued to the user!
    # Each "Row" contains [ deviceID, manufacturer, modelNumber]
    # If no devices = empty list []

    # devices = [
    #     [7, 'Zava', '1146805551'],
    #     [13, 'Skyndu', '5296853075'],
    #     [24, 'Yakitri', '8406089423'],
    # ]

    # return devices

    connection = database_connect();

    if(connection is None):
        print("get_devices_used_by: The connection is fail!");
        return None;

    cursor = connection.cursor();

    try:
        # cursor.execute("SELECT * FROM student WHERE sid=%s", (sid))

        query = '''SELECT deviceID, manufacturer, modelNumber
                    FROM DeviceUsedBy INNER JOIN Device USING(deviceID)
                    WHERE empID = %s;''';

        cursor.execute(query, (employee_id,));
        devices = cursor.fetchall();
        cursor.close() # IMPORTANT: close cursor
        connection.close() # IMPORTANT: close connection


    except Exception as e:
        # This happens if there is an error executing the query
        print("Error executing function");
        print(e);
        cursor.close();                    # Close the cursor
        connection.close();


    retur_list = [];

    if(devices is not None):
        for element in devices:
            retur_list.append(element);
    return retur_list;


#####################################################
#   Query (a[iii])
#   Get departments employee works in
#####################################################

def employee_works_in(employee_id: int) -> List[str]:
    """
    Return the departments that the employee works in.
    """

    # TODO Dummy Data - Change to be useful!
    # Return a list of departments

    # departments = ['IT', 'Marketing']

    # return departments

    query = ''' SELECT department
                FROM EmployeeDepartments
                WHERE empID = %s;''';

    connection = database_connect();

    if(connection is None):
        print("get_devices_used_by: The connection is fail!");
        return None;

    cursor = connection.cursor();

    try:
        cursor.execute(query, (employee_id,));
        working_department = cursor.fetchall();
        cursor.close() # IMPORTANT: close cursor
        connection.close() # IMPORTANT: close connection
    except Exception as e:
        print("Error executing function");
        print(e);
        cursor.close();                    # Close the cursor
        connection.close();

    # departments = ['IT', 'Marketing']

    departments = [];

    if(working_department is not None):
        for depart in working_department:
            departments.append(depart);

    return departments;


#####################################################
#   Query (c)
#   Get My Issued Devices
#####################################################

def get_issued_devices_for_user(employee_id: int) -> list:
    """
    Get all devices issued to the user.
        - Return a list of all devices to the user.
    """

    # TODO Dummy Data - Change to be useful!
    # Return a list of devices issued to the user!
    # Each "Row" contains [ deviceID, purchaseDate, manufacturer, modelNumber ]
    # If no devices = empty list []

    # devices = [
    #     [7, datetime.date(2017, 8, 28), 'Zava', '1146805551'],
    #     [8, datetime.date(2017, 9, 22), 'Topicware', '5798231046'],
    #     [6123, datetime.date(2017, 9, 5), 'Dabshots', '6481799600'],
    #     [1373, datetime.date(2018, 4, 19), 'Cogibox', '6700815444'],
    #     [8, datetime.date(2018, 2, 10), 'Feednation', '2050267274'],
    #     [36, datetime.date(2017, 11, 5), 'Muxo', '8768929463'],
    #     [17, datetime.date(2018, 1, 14), 'Izio', '5886976558'],
    #     [13, datetime.date(2017, 9, 8), 'Skyndu', '5296853075'],
    #     [24, datetime.date(2017, 10, 22), 'Yakitri', '8406089423'],
    # ]

    # return devices
    query = ''' SELECT deviceID, purchaseDate, manufacturer, modelNumber
                FROM Device
                WHERE issuedTo = %s;''';

    connection = database_connect();

    if(connection is None):
        print("get_issued_devices_for_user: The connection is fail!");
        return None;

    cursor = connection.cursor();

    try:
        cursor.execute(query, (employee_id,));
        issued_devices_list = cursor.fetchall();
        cursor.close() # IMPORTANT: close cursor
        connection.close() # IMPORTANT: close connection
    except Exception as e:
        print("Error executing function");
        print(e);
        cursor.close();                    # Close the cursor
        connection.close();

    return_list = [];
    if(len(issued_devices_list) > 0):
        # print(issued_devices_list);
        for element in issued_devices_list:
            return_list.append(element);
    return return_list;

#####################################################
#   Query (b)
#   Get All Models
#####################################################

def get_all_models() -> list:
    """
    Get all models available.
    """

    # TODO Dummy Data - Change to be useful!
    # Return the list of models with information from the model table.
    # Each "Row" contains: [manufacturer, description, modelnumber, weight]
    # If No Models = EMPTY LIST []

    # models = [
    #     ['Feednation', 'Expanded didactic instruction set', '2050267274', 31],
    #     ['Zoombox', 'Profit-focused global extranet', '8860068207', 57],
    #     ['Shufflebeat', 'Robust clear-thinking functionalities', '0288809602', 23],
    #     ['Voonyx', 'Vision-oriented bandwidth-monitored instruction set', '5275001460', 82],
    #     ['Tagpad', 'Fundamental human-resource migration', '3772470904', 89],
    #     ['Wordpedia', 'Business-focused tertiary orchestration', '0211912271', 17],
    #     ['Skyndu', 'Quality-focused web-enabled parallelism', '5296853075', 93],
    #     ['Tazz', 'Re-engineered well-modulated contingency', '8479884797', 95],
    #     ['Dabshots', 'Centralized empowering protocol', '6481799600', 68],
    #     ['Rhybox', 'Re-contextualized bifurcated orchestration', '7107712551', 25],
    #     ['Cogibox', 'Networked disintermediate application', '6700815444', 27],
    #     ['Meedoo', 'Progressive 24-7 orchestration', '3998544224', 43],
    #     ['Zoomzone', 'Reverse-engineered systemic monitoring', '9854941272', 50],
    #     ['Meejo', 'Secured static implementation', '3488947459', 75],
    #     ['Topicware', 'Extended system-worthy forecast', '5798231046', 100],
    #     ['Izio', 'Open-source static productivity', '5886976558', 53],
    #     ['Zava', 'Polarised incremental paradigm', '1146805551', 82],
    #     ['Demizz', 'Reduced hybrid website', '9510770736', 63],
    #     ['Muxo', 'Switchable contextually-based throughput', '8768929463', 40],
    #     ['Wordify', 'Front-line fault-tolerant middleware', '8465785368', 84],
    #     ['Twinder', 'Intuitive contextually-based local area network', '5709369365', 78],
    #     ['Jatri', 'Horizontal disintermediate workforce', '8271780565', 31],
    #     ['Chatterbridge', 'Phased zero tolerance architecture', '8429506128', 39],
    # ]

    # return models
    query = ''' SELECT manufacturer, description, modelnumber, weight
                FROM Model;''';

    connection = database_connect();

    if(connection is None):
        print("get_issued_devices_for_user: The connection is fail!");
        return None;

    cursor = connection.cursor();

    try:
        cursor.execute(query);
        models = cursor.fetchall();
        cursor.close() # IMPORTANT: close cursor
        connection.close() # IMPORTANT: close connection

    except Exception as e:
        print("Error executing function");
        print(e);
        cursor.close();                    # Close the cursor
        connection.close();

    return_list = [];

    if(models is not None):
        for element_list in models:
            return_list.append(element_list);

    return return_list;


#####################################################
#   Query (d[ii])
#   Get Device Repairs
#####################################################

def get_device_repairs(device_id: int) -> list:
    """
    Get all repairs made to a device.
    """

    # TODO Dummy Data - Change to be useful!
    # Return the repairs done to a certain device
    # Each "Row" contains:
    #       - repairid
    #       - faultreport
    #       - startdate
    #       - enddate
    #       - cost
    # If no repairs = empty list

    # repairs = [
    #     [17, 'Never, The', datetime.date(2018, 7, 16), datetime.date(2018, 9, 22), '$837.13'],
    #     [18, 'Gonna', datetime.date(2018, 8, 3), datetime.date(2018, 9, 22), '$1726.99'],
    #     [19, 'Give', datetime.date(2018, 9, 4), datetime.date(2018, 9, 17), '$1751.01'],
    #     [20, 'You', datetime.date(2018, 7, 21), datetime.date(2018, 9, 23), '$1496.36'],
    #     [21, 'Up', datetime.date(2018, 8, 17), datetime.date(2018, 9, 18), '$1133.88'],
    #     [22, 'Never', datetime.date(2018, 8, 8), datetime.date(2018, 9, 24), '$1520.95'],
    #     [23, 'Gonna', datetime.date(2018, 9, 1), datetime.date(2018, 9, 29), '$611.09'],
    #     [24, 'Let', datetime.date(2018, 7, 5), datetime.date(2018, 9, 15), '$1736.03'],
    # ]

    # return repairs
    query = ''' SELECT repairid, faultreport, startdate, enddate, cost
                FROM Repair
                WHERE doneTo = %s;''';

    connection = database_connect();

    if(connection is None):
        print("get_device_repairs: The connection is fail!");
        return None;

    cursor = connection.cursor();

    try:
        cursor.execute(query, (device_id,));
        repair_times = cursor.fetchall();
        cursor.close() # IMPORTANT: close cursor
        connection.close() # IMPORTANT: close connection
    except Exception as e:
        print("Error executing function");
        print(e);
        cursor.close();                    # Close the cursor
        connection.close();

    return_list = [];

    if(device_id is not None):
        for element_list in repair_times:
            return_list.append(element_list);
    return return_list;

#####################################################
#   Query (d[i])
#   Get Device Info
#####################################################

def get_device_information(device_id: int) -> Optional[dict]:
    """
    Get related device information in detail.
    """

    # TODO Dummy Data - Change to be useful!
    # Return all the relevant device information for the device

    # device_info = [
    #     1,                      # DeviceID
    #     '2721153188',           # SerialNumber
    #     datetime.date(2017, 12, 19),  # PurchaseDate
    #     '$1009.10',             # PurchaseCost
    #     'Zoomzone',             # Manufacturer
    #     '9854941272',           # ModelNumber
    #     1337,                   # IssuedTo
    # ]

    # device = {
    #     'device_id': device_info[0],
    #     'serial_number': device_info[1],
    #     'purchase_date': device_info[2],
    #     'purchase_cost': device_info[3],
    #     'manufacturer': device_info[4],
    #     'model_number': device_info[5],
    #     'issued_to': device_info[6],
    # }

    # return device
    query = ''' SELECT DeviceID, SerialNumber, PurchaseDate, PurchaseCost, Manufacturer, ModelNumber,IssuedTo
                FROM Device
                WHERE deviceID = %s;''';

    connection = database_connect();

    if(connection is None):
        print("get_device_information: The connection is fail!");
        return None;

    cursor = connection.cursor();

    try:
        cursor.execute(query, (device_id,));
        device_info = cursor.fetchone();
        cursor.close() # IMPORTANT: close cursor
        connection.close() # IMPORTANT: close connection
    except Exception as e:
        print("Error executing function");
        print(e);
        cursor.close();                    # Close the cursor
        connection.close();

    if(device_info is None):

        # none_device = {
        #         'device_id': '',
        #         'serial_number': '',
        #         'purchase_date': '',
        #         'purchase_cost': '',
        #         'manufacturer': '',
        #         'model_number': '',
        #         'issued_to': ''};

        return None;

    device = {
        'device_id': device_info[0],
        'serial_number': device_info[1],
        'purchase_date': device_info[2],
        'purchase_cost': device_info[3],
        'manufacturer': device_info[4],
        'model_number': device_info[5],
        'issued_to': device_info[6],
    }

    return device;


#####################################################
#   Query (d[iii/iv])
#   Get Model Info by Device
#####################################################

def get_device_model(device_id: int) -> Optional[dict]:
    """
    Get model information about a device.
    """

    # TODO Dummy Data - Change to be useful!

    # model_info = [
    #     'Zoomzone',              # manufacturer
    #     '9854941272',            # modelNumber
    #     'brick--I mean laptop',  # description
    #     2000,                    # weight
    # ]

    # model = {
    #     'manufacturer': model_info[0],
    #     'model_number': model_info[1],
    #     'description': model_info[2],
    #     'weight': model_info[3],
    # }
    # return model

    query = ''' SELECT manufacturer, modelNumber, description, weight
                FROM Model m
                WHERE EXISTS (SELECT *
                                FROM Device d
                                WHERE d.manufacturer = m.manufacturer
                                AND d.modelNumber = m.modelNumber
                                AND d.deviceID = %s);''';

    connection = database_connect();

    if(connection is None):
        print("get_device_model: The connection is fail!");
        return None;

    cursor = connection.cursor();

    try:
        cursor.execute(query, (device_id,));
        model_info = cursor.fetchone();
        cursor.close() # IMPORTANT: close cursor
        connection.close() # IMPORTANT: close connection
    except Exception as e:
        print("Error executing function");
        print(e);
        cursor.close();                    # Close the cursor
        connection.close();

    if(model_info is None):
        # none_model = {'manufacturer': '',
        #             'model_number': '',
        #             'description': '',
        #             'weight': ''};
        return None;

    model = {
        'manufacturer': model_info[0],
        'model_number': model_info[1],
        'description': model_info[2],
        'weight': model_info[3],
    }
    return model;


#####################################################
#   Query (e)
#   Get Repair Details
#####################################################

def get_repair_details(repair_id: int) -> Optional[dict]:
    """
    Get information about a repair in detail, including service information.
    """

    # TODO Dummy data - Change to be useful!

    # repair_info = [
    #     17,                    # repair ID
    #     'Never, The',          # fault report
    #     datetime.date(2018, 7, 16),  # start date
    #     datetime.date(2018, 9, 22),  # end date
    #     '$837.13',             # cost
    #     '12345678901',         # service ABN
    #     'TopDrive',            # service name
    #     'repair@example.com',  # service email
    #     1,                     # done to device
    # ]

    # repair = {
    #     'repair_id': repair_info[0],
    #     'fault_report': repair_info[1],
    #     'start_date': repair_info[2],
    #     'end_date': repair_info[3],
    #     'cost': repair_info[4],
    #     'done_by': {
    #         'abn': repair_info[5],
    #         'service_name': repair_info[6],
    #         'email': repair_info[7],
    #     },
    #     'done_to': repair_info[8],
    # }
    # return repair

    query = ''' SELECT repairID, faultReport, startDate, endDate, cost, abn, serviceName, email, doneTo
                FROM Repair FULL OUTER JOIN Service on(doneBy = abn)
                WHERE repairID = %s;''';

    connection = database_connect();

    if(connection is None):
        print("get_repair_details: The connection is fail!");
        return None;

    cursor = connection.cursor();

    try:
        cursor.execute(query, (repair_id,));
        repair_info = cursor.fetchone();
        cursor.close() # IMPORTANT: close cursor
        connection.close() # IMPORTANT: close connection
    except Exception as e:
        print("Error executing function");
        print(e);
        cursor.close();                    # Close the cursor
        connection.close();

    if(repair_info is None):
        return None;

    repair = {
        'repair_id': repair_info[0],
        'fault_report': repair_info[1],
        'start_date': repair_info[2],
        'end_date': repair_info[3],
        'cost': repair_info[4],
        'done_by': {
            'abn': repair_info[5],
            'service_name': repair_info[6],
            'email': repair_info[7],
        },
        'done_to': repair_info[8],
    }
    return repair;


#####################################################
#   Query (f[ii])
#   Get Models assigned to Department
#####################################################

def get_department_models(department_name: str) -> list:
    """
    Return all models assigned to a department.
    """

    # TODO Dummy Data - Change to be useful!
    # Return the models allocated to the department.
    # Each "row" has: [ manufacturer, modelnumber, maxnumber ]

    # model_allocations = [
    #     ['Devpulse', '4030141218', 153],
    #     ['Gabcube', '1666158895', 186],
    #     ['Feednation', '2050267274', 275],
    #     ['Zoombox', '8860068207', 199],
    #     ['Shufflebeat', '0288809602', 208],
    #     ['Voonyx', '5275001460', 264],
    #     ['Tagpad', '3772470904', 227],
    # ]

    # return model_allocations
    query = ''' SELECT manufacturer, modelNumber, maxnumber
                FROM ModelAllocations
                WHERE department = %s;''';

    connection = database_connect();

    if(connection is None):
        print("get_department_models: The connection is fail!");
        return None;

    cursor = connection.cursor();

    try:
        cursor.execute(query, (department_name,));
        model_allocations = cursor.fetchall();
        cursor.close() # IMPORTANT: close cursor
        connection.close() # IMPORTANT: close connection

    except Exception as e:
        print("Error executing function");
        print(e);
        cursor.close();                    # Close the cursor
        connection.close();

    return_list = [];

    if(len(model_allocations) < 1):
        return return_list;
    else:
        for ele_list in model_allocations:
            return_list.append(ele_list);
    return return_list;


#####################################################
#   Query (f[iii])
#   Get Number of Devices of Model owned
#   by Employee in Department
#####################################################

def get_employee_department_model_device(department_name: str, manufacturer: str, model_number: str) -> list:
    """
    Get the number of devices owned per employee in a department
    matching the model.

    E.g. Model = iPhone, Manufacturer = Apple, Department = "Accounting"
        - [ 1337, Misty, 20 ]
        - [ 351, Pikachu, 10 ]
    """

    # TODO Dummy Data - Change to be useful!
    # Return the number of devices owned by each employee matching department,
    #   manufacturer and model.
    # Each "row" has: [ empid, name, number of devices issued that match ]

    # employee_counts = [
    #     [1337, 'Misty', 20],
    #     [351, 'Pikachu', 1],
    #     [919, 'Hermione', 8],
    # ]

    # return employee_counts
    query = ''' SELECT D.issuedTo , E.name, count(D.deviceID)
                 FROM Device D, Employee E
                 WHERE D.manufacturer = %s AND
                       D.modelnumber = %s AND
                       D.issuedTo IS NOT NULL AND
                       D.issuedTo IN (
                            SELECT empid
                            FROM EmployeeDepartments
                            WHERE department = %s
                        ) AND
                        E.empid = D.issuedTo
                GROUP BY D.issuedTo, E.name;''';

    connection = database_connect();

    if(connection is None):
        print("get_employee_department_model_device: The connection is fail!");
        return None;

    cursor = connection.cursor();

    try:
        cursor.execute(query, (manufacturer,model_number,department_name));
        employee_counts = cursor.fetchall();
        cursor.close() # IMPORTANT: close cursor
        connection.close() # IMPORTANT: close connection
    except Exception as e:
        print("Error executing function");
        print(e);
        cursor.close();                    # Close the cursor
        connection.close();

    return_list = [];

    if(employee_counts is not None):
        for element in employee_counts:
            return_list.append(element);

    if(len(return_list) == 0):
        return None;

    return return_list;


#####################################################
#   Query (f[iv])
#   Get a list of devices for a certain model and
#       have a boolean showing if the employee has
#       it issued.
#####################################################

def get_model_device_assigned(model_number: str, manufacturer: str, employee_id: int) -> list:
    """
    Get all devices matching the model and manufacturer and show True/False
    if the employee has the device assigned.

    E.g. Model = Pixel 2, Manufacturer = Google, employee_id = 1337
        - [123656, False]
        - [123132, True]
        - [51413, True]
        - [8765, False]
    """

    # TODO Dummy Data - Change to be useful!
    # Return each device of this model and whether the employee has it
    # issued.
    # Each "row" has: [ device_id, True if issued, else False.]

    # device_assigned = [
    #     [123656, False],
    #     [123132, True],
    #     [51413, True],
    #     [8765, False],
    # ]

    # return device_assigned
    query = '''SELECT deviceID,
                    CASE
                        WHEN issuedTo is null then false
                     WHEN issuedTo is Not null then issuedTo = %s
                     END

                FROM Device
                WHERE manufacturer = %s AND modelnumber = %s;''';

    connection = database_connect();

    if(connection is None):
        print("get_model_device_assigned: The connection is fail!");
        return None;

    cursor = connection.cursor();

    try:
        cursor.execute(query, (employee_id, manufacturer, model_number));
        device_assigned = cursor.fetchall();
        cursor.close() # IMPORTANT: close cursor
        connection.close() # IMPORTANT: close connection
    except Exception as e:
        print("Error executing function");
        print(e);
        cursor.close();                    # Close the cursor
        connection.close();

    return_list = [];

    if(device_assigned is not None):
        for element in device_assigned:
            return_list.append(element);
    return return_list;

#####################################################
#   Get a list of devices for this model and
#       manufacturer that have not been assigned.
#####################################################

def get_unassigned_devices_for_model(model_number: str, manufacturer: str) -> list:
    """
    Get all unassigned devices for the model.
    """

    # TODO Dummy Data - Change to be useful!
    # Return each device of this model that has not been issued
    # Each "row" has: [ device_id ]
    # device_unissued = [123656, 123132, 51413, 8765]

    # return device_unissued
    query = ''' SELECT deviceID
                FROM Device FULL OUTER JOIN Model USING(manufacturer, modelNumber)
                WHERE manufacturer = %s AND modelnumber = %s AND issuedTo is NULL;''';

    connection = database_connect();

    if(connection is None):
        print("get_unassigned_devices_for_model: The connection is fail!");
        return None;

    cursor = connection.cursor();

    try:
        cursor.execute(query, (manufacturer, model_number));
        device_unissued = cursor.fetchall();
        cursor.close() # IMPORTANT: close cursor
        connection.close() # IMPORTANT: close connection
    except Exception as e:
        print("Error executing function");
        print(e);
        cursor.close();                    # Close the cursor
        connection.close();

    return_list = [];

    if(device_unissued is not None):
        for element in device_unissued:
            if(element is not None):
                return_list.append(element[0]);

    return return_list;

#####################################################
#   Get Employees in Department
#####################################################

def get_employees_in_department(department_name: str) -> list:
    """
    Return all the employees' IDs and names in a given department.
    """

    # TODO Dummy Data - Change to be useful!
    # Return the employees in the department.
    # Each "row" has: [ empid, name ]

    # employees = [
    #     [15905, 'Rea Fibbings'],
    #     [9438, 'Julia Norville'],
    #     [36020, 'Adora Lansdowne'],
    #     [98809, 'Nathanial Farfoot'],
    #     [58407, 'Lynne Smorthit'],
    # ]

    # return employees

    query = ''' SELECT empid, name
                FROM EmployeeDepartments FULL OUTER JOIN Employee USING(empid)
                WHERE department = %s;''';

    connection = database_connect();

    if(connection is None):
        print("get_employees_in_department: The connection is fail!");
        return None;

    cursor = connection.cursor();

    try:
        cursor.execute(query, (department_name,));
        employees = cursor.fetchall();
        cursor.close() # IMPORTANT: close cursor
        connection.close() # IMPORTANT: close connection
    except Exception as e:
        print("Error executing function");
        print(e);
        cursor.close();                    # Close the cursor
        connection.close();

    return_list = [];

    if(employees is not None):
        for element in employees:
            return_list.append(element);
    return return_list;

#####################################################
#   Query (f[v])
#   Issue Device
#####################################################

def issue_device_to_employee(employee_id: int, device_id: int):
    """
    Issue the device to the chosen employee.
    """

    # TODO issue the device from the employee
    # Return (True, None) if all good
    # Else return (False, ErrorMsg)
    # Error messages:
    #       - Device already issued?
    #       - Employee not in department?

    # return (False, "Device already issued")
    # return (True, None)

    # test_employee_quert = ''' SELECT department FROM EmployeeDepartments WHERE empID = %s ''';
    # test_device_quert = ''' SELECT issuedTo FROM Device WHERE deviceID = %s ''';
    add_use_to_employee = """INSERT INTO DeviceUsedBy (deviceid, empid)
                        VALUES(%s, %s)""";

    execute_query = ''' UPDATE Device
                        SET issuedTo = %s
                        WHERE deviceID = %s;''';



    device_info = get_device_information(device_id);
    if(device_info != None):
        if(device_info.get('issued_to') != None):
            return (False, "Device already issued");


    connection = database_connect();

    if(connection is None):
        print("issue_device_to_employee: The connection is fail!");
        return None;

    cursor = connection.cursor();



    try:
        #Try executing the SQL and get from the database
        cursor.execute(execute_query, (employee_id,device_id));
        connection.commit();
        cursor.execute(add_use_to_employee, (device_id, employee_id,))
        connection.commit();
        cursor.close() # IMPORTANT: close cursor
        connection.close() # IMPORTANT: close connection
    except Exception as e:
        print("Error executing function");
        print(e);
        cursor.close();
        connection.commit();                  # Close the cursor
        connection.close();

    return (True, None);


#####################################################
#   Query (f[vi])
#   Revoke Device Issued to User
#####################################################

def revoke_device_from_employee(employee_id: int, device_id: int):
    """
    Revoke the device from the employee.
    """

    # TODO revoke the device from the employee.
    # Return (True, None) if all good
    # Else return (False, ErrorMsg)
    # Error messages:
    #       - Device already revoked?
    #       - employee not assigned to device?

    # # return (False, "Device already unassigned")
    # return (True, None)

    execute_query = ''' UPDATE Device
                        SET issuedTo = null
                        WHERE issuedTo = %s AND deviceID = %s;''';

    issued_devices = get_issued_devices_for_user(employee_id)
    can_revoke = False

    for issued in issued_devices:
        if(int(issued[0]) == int(device_id)):
            can_revoke = True;

    if not can_revoke:
        return (False, "employee not assigned to device");

    device_info = get_device_information(device_id)
    if(device_info.get('issued_to') == None):
        return (False, "Device already revoked");

    connection = database_connect();

    if(connection is None):
        print("revoke_device_from_employee: The connection is fail!");
        return None;

    cursor = connection.cursor();

    try:
        cursor.execute(execute_query, (employee_id,device_id));
        connection.commit();
        cursor.close() # IMPORTANT: close cursor
        connection.close() # IMPORTANT: close connection
    except Exception as e:
        print("Error executing function");
        print(e);
        cursor.close();                    # Close the cursor
        connection.close();

    return (True, None);




def get_noDepartment_employee() -> list:
    """
    Get all employees without department associated.
    """

    # return device_unissued
    # [[3081, 'Tam Janson', '10 Jenna Circle', datetime.date(1988, 5, 2)],
    # [27933, 'Kore Andersen', '68944 Jenifer Street', datetime.date(1966, 5, 24)],
    # [67723, 'Vida Dods', '03 Village Avenue', datetime.date(1968, 7, 6)],
    # [51156, 'Sean Coster', '7 Hollow Ridge Alley', datetime.date(1957, 3, 2)],
    # [34290, 'Rosemonde Phipson', '219 Weeping Birch Plaza', datetime.date(1982, 8, 2)],
    # [52675, 'Stafani Drought', '279 Stang Parkway', datetime.date(1999, 8, 25)],
    # [71800, 'Josee Coltart', '5 Dapin Drive', datetime.date(1992, 2, 23)],
    # [62109, "Lonni D'Emanuele", '6 Heffernan Crossing', datetime.date(1990, 6, 2)],
    # [37844, 'Hayden Grewcock', '55 Burrows Terrace', datetime.date(1955, 8, 6)],
    # [66051, 'Aggie Priditt', '2 Canary Center', datetime.date(1982, 1, 6)],
    # [15905, 'Rea Fibbings', '7578 Magdeline Trail', datetime.date(1969, 6, 7)]]

    query = ''' SELECT empid, name, homeaddress, dateofbirth
                FROM Employee FULL OUTER JOIN EmployeeDepartments USING(empID)
                WHERE department is NULL; ''';

    connection = database_connect();

    if(connection is None):
        print("get_noDepartment_employee: The connection is fail!");
        return None;

    cursor = connection.cursor();

    try:
        cursor.execute(query);
        unsidned_employees = cursor.fetchall();
        cursor.close() # IMPORTANT: close cursor
        connection.close() # IMPORTANT: close connection
    except Exception as e:
        print("Error executing function");
        print(e);
        cursor.close();                    # Close the cursor
        connection.close();

    return_list = [];

    if(unsidned_employees is not None):
        for emp in unsidned_employees:
            if(emp is not None):
                return_list.append(emp);

    return return_list;


def assigned_employee_to_department(employee_id: int, department_name: str):
    """
    Get all employees without department associated.
    """

    # return device_unissued
    # [[3081, 'Tam Janson', '10 Jenna Circle', datetime.date(1988, 5, 2)],
    # [27933, 'Kore Andersen', '68944 Jenifer Street', datetime.date(1966, 5, 24)],
    # [67723, 'Vida Dods', '03 Village Avenue', datetime.date(1968, 7, 6)],
    # [51156, 'Sean Coster', '7 Hollow Ridge Alley', datetime.date(1957, 3, 2)],
    # [34290, 'Rosemonde Phipson', '219 Weeping Birch Plaza', datetime.date(1982, 8, 2)],
    # [52675, 'Stafani Drought', '279 Stang Parkway', datetime.date(1999, 8, 25)],
    # [71800, 'Josee Coltart', '5 Dapin Drive', datetime.date(1992, 2, 23)],
    # [62109, "Lonni D'Emanuele", '6 Heffernan Crossing', datetime.date(1990, 6, 2)],
    # [37844, 'Hayden Grewcock', '55 Burrows Terrace', datetime.date(1955, 8, 6)],
    # [66051, 'Aggie Priditt', '2 Canary Center', datetime.date(1982, 1, 6)],
    # [15905, 'Rea Fibbings', '7578 Magdeline Trail', datetime.date(1969, 6, 7)]]

    query = ''' INSERT INTO EmployeeDepartments (empID, department, fraction) VALUES(%s, %s, 0)''';

    connection = database_connect();

    if(connection is None):
        print("assigned_employee_to_department: The connection is fail!");
        return None;

    cursor = connection.cursor();

    try:
        cursor.execute(query, (employee_id, department_name));
        connection.commit();
        cursor.close(); # IMPORTANT: close cursor
        connection.close(); # IMPORTANT: close connection
    except Exception as e:
        print("Error executing function");
        print(e);
        cursor.close();                    # Close the cursor
        connection.close();

    return (True, None);
