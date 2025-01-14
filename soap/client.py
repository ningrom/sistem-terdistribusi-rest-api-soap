import requests
import xml.etree.ElementTree as ET
from soapxml import create_xml, read_all_xml, update_xml, delete_xml

def parse_response(response_text):
    """Parse the SOAP response and return the relevant data from specific tags."""
    print("Response Text:", response_text)
    
    root = ET.fromstring(response_text)
    # Find the namespace
    namespace = {'soapenv': 'http://schemas.xmlsoap.org/soap/envelope/', 'tns': 'spyne.examples.mysql.soap'}
    
    # Extract the body of the response
    body = root.find('soapenv:Body', namespace)
    if body is not None:
        # Check for the create response
        create_result = body.find('.//tns:createResponse/tns:createResult', namespace)
        if create_result is not None:
            return create_result.text.strip()
        
        # Check for the read response
        read_result = body.find('.//tns:readByNamaResponse/tns:readByNamaResult', namespace)
        if read_result is not None:
            return read_result.text.strip()
        
        # Check for the readAll response
        read_all_result = body.find('.//tns:readAllResponse/tns:readAllResult', namespace)
        if read_all_result is not None:
            return read_all_result.text.strip()
        
        # Check for the update response
        update_result = body.find('.//tns:updateResponse/tns:updateResult', namespace)
        if update_result is not None:
            return update_result.text.strip()
        
        # Check for the delete response
        delete_result = body.find('.//tns:deleteResponse/tns:deleteResult', namespace)
        if delete_result is not None:
            return delete_result.text.strip()
        
        return "No relevant data found."
    
    return "No response body found."

def id_exists(nim):
    xml_request = f'''<soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/" xmlns:tns="spyne.examples.mysql.soap">
        <soapenv:Header/>
        <soapenv:Body>
            <tns:read>
                <tns:nim>{nim}</tns:nim>
            </tns:read>
        </soapenv:Body>
    </soapenv:Envelope>'''
    response = requests.post('http://127.0.0.1:8000', data=xml_request, headers={'Content-Type': 'text/xml'})
    return "Mahasiswa record not found" not in response.text


def readAll():
    """Function to read all records from the Excel file."""
    xml_request = read_all_xml()
    response = requests.post('http://127.0.0.1:8000', data=xml_request, headers={'Content-Type': 'text/xml'})
    return response.text

def main():
    while True:
        print("\nChoose an operation:")
        print("1. Create")
        print("2. Read All")
        print("3. Update")
        print("4. Delete")
        print("5. Exit")
        
        choice = input("Enter your choice (1-5): ")

        if choice == '1':  # Create
            name = input("Enter Name: ")
            nim = input("Enter nim: ")
            prodi = input("Enter Prodi: ")
            xml_request = create_xml(name, nim, prodi)
            response = requests.post('http://127.0.0.1:8000', data=xml_request, headers={'Content-Type': 'text/xml'})
            print("Response Text:", response.text)  
            parsed_result = parse_response(response.text)
            print(parsed_result)

        elif choice == '2':  # Read All
            print("Fetching all records...")
            response = readAll()
            parsed_result = parse_response(response)
            print(parsed_result)

        elif choice == '3':  # Update
            nim = input("Enter nim: ")
            if not id_exists(nim):
                print(f"Mahasiswa dengan NIM {nim} tidak ditemukan. Tidak dapat melakukan update.")
                continue
            name = input("Enter new Name: ")
            prodi = input("Enter new Prodi: ")
            xml_request = update_xml(nim, name, prodi)
            print("Sending XML Request for Update:", xml_request)
            response = requests.post('http://127.0.0.1:8000', data=xml_request, headers={'Content-Type': 'text/xml'})
            parsed_result = parse_response(response.text)
            print(parsed_result)

        elif choice == '4':  # Delete
            nim = input("Enter nim to delete: ")
            if not id_exists(nim):
                print("Record not found. Please enter a valid nim.")
                continue
            xml_request = delete_xml(nim)
            response = requests.post('http://127.0.0.1:8000', data=xml_request, headers={'Content-Type': 'text/xml'})
            parsed_result = parse_response(response.text)
            print(parsed_result)

        elif choice == '5':  # Exit
            print("Exiting the program.")
            break

        else:
            print("Invalid choice. Please enter a number between 1 and 5.")

if __name__ == "__main__":
    main()