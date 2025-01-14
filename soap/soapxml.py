
# Fungsi untuk membuat XML SOAP untuk Create
def create_xml(nama, nim, prodi):
    return f'''<soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/" xmlns:tns="spyne.examples.mysql.soap">
        <soapenv:Header/>
        <soapenv:Body>
            <tns:create>
                
                <tns:nama>{nama}</tns:nama>
                <tns:nim>{nim}</tns:nim>
                <tns:prodi>{prodi}</tns:prodi>
            </tns:create>
        </soapenv:Body>
    </soapenv:Envelope>'''

def read_all_xml():
    return '''<soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/" xmlns:tns="spyne.examples.mysql.soap">
        <soapenv:Header/>
        <soapenv:Body>
            <tns:readAll/>
        </soapenv:Body>
    </soapenv:Envelope>'''


def update_xml(nim, nama, prodi):
    return f'''<soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/" xmlns:tns="spyne.examples.mysql.soap">
        <soapenv:Header/>
        <soapenv:Body>
            <tns:update>
                <tns:nim>{nim}</tns:nim>  
                <tns:nama>{nama}</tns:nama>  
                <tns:prodi>{prodi}</tns:prodi> 
            </tns:update>
        </soapenv:Body>
    </soapenv:Envelope>'''



def delete_xml(nim):
    return f'''<soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/" xmlns:tns="spyne.examples.mysql.soap">
        <soapenv:Header/>
        <soapenv:Body>
            <tns:delete>
                <tns:nim>{nim}</tns:nim>
            </tns:delete>
        </soapenv:Body>
    </soapenv:Envelope>'''

