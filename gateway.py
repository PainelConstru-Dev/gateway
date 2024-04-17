import requests
import os


# Criar novo cliente
def create_customer():
    url = os.getenv("ASAAS_URL") + "/customers"
    headers = {
        "accept": "application/json",
        "content-type": "application/json",
        "access_token": os.getenv("ASAAS_KEY"),
    }
    payload = {
        "name": "João da Silva",
        "email": "email@auto.com.br",
        "phone": "5511949949939",
        "mobilePhone": "5511949939293",
        "cpfCnpj": "12345678909",
        "postalCode": "05443000",
        "address": "Rua Fidêncio Ramos",
        "addressNumber": "308",
        "complement": "9º andar",
        "province": "SP",
        "externalReference": "123456789",
    }

    response = requests.post(url, json=payload, headers=headers)
    print(response.text)

def list_customers():
    url = os.getenv("ASAAS_URL") + "/customers"
    headers = {
        "accept": "application/json",
        "content-type": "application/json",
        "access_token": os.getenv("ASAAS_KEY"),
    }

    response = requests.get(url, headers=headers)
    # print(response.text)
    print('Lista de clientes:')
    for customer in response.json()['data']:
        print(f"Nome: {customer['name']}\t Email: {customer['email']}\t CPF/CNPJ: {customer['cpfCnpj']} \t ID: {customer['id']}")

def create_pix_key():
    """Permite a manipulação de chaves aleátorias da sua conta Asaas."""
    url = os.getenv("ASAAS_URL") + "/pix/addressKeys"
    payload = { "type": "EVP" }
    headers = {
        "accept": "application/json",
        "content-type": "application/json",
        "access_token": os.getenv("ASAAS_KEY"),
    }

    response = requests.post(url, json=payload, headers=headers)

    print(response.text)

def payment(customer, value, dueDate, description, type='PIX', externalReference='', fine=3, interest=2):
    """É possível escolher entre as formas de pagamento com boleto, cartão de crédito, Pix ou permitir que o cliente escolha a forma que desejar.
    """
    url = os.getenv("ASAAS_URL") + "/payments"
    headers = {
        "accept": "application/json",
        "content-type": "application/json",
        "access_token": os.getenv("ASAAS_KEY"),
    }
    payload = {
        "billingType": type,  # Tipo de pagamento (PIX, BOLETO, CREDIT_CARD, UNDEFINED)
        "customer": customer,  # id do cliente, criada na api de clientes
        "value": value,  # Valor do pagamento teste #float
        "dueDate": dueDate,  # Data de vencimento #yyyy-mm-dd
        "description": description,  # Descrição do pagamento
        "daysAfterDueDateToRegistrationCancellation": 2,  # Dias após o vencimento para cancelamento do pagamento
        "externalReference": externalReference,  # Referência externa (ref painel?)
        "interest": { "value": interest }, # Percentual de juros ao mês sobre o valor da cobrança para pagamento após o vencimento
        "fine": { # Percentual de multa sobre o valor da cobrança para pagamento após o vencimento
        "value": fine,
        "type": "PERCENTAGE"
    },
    }

    response = requests.post(url, json=payload, headers=headers)  # Requisição POST

    print(response.text)  # Resposta da API

def list_payments(customer_id):
    """Listar cobranças de um cliente específico: """
    
    url = os.getenv("ASAAS_URL") + f"/payments?customer={customer_id}"
    headers = {
        "accept": "application/json",
        "access_token": os.getenv("ASAAS_KEY"),
    }

    response = requests.get(url, headers=headers)
    print('Lista de pagamentos:')
    for payment in response.json()['data']:
        print(f"Descrição: {payment['description']}\t Valor: R$ {payment['value']}\t Tipo: {payment['billingType']}\t Data de vencimento: {payment['dueDate']} \t ID: {payment['id']}")


if __name__ == "__main__":
    #menu
    print(":")
    while True:
        print("1 - Criar novo cliente")
        print("2 - Listar clientes")
        print("3 - Criar chave PIX")
        print("4 - Listar pagamentos do cliente")

        option = input("Digite a opção desejada (ou Quit): ")
        
        if option == "1":
            create_customer()
        elif option == "2":
            list_customers()
        elif option == "3":
            create_pix_key()
        elif option == "4":
            customer_id = input("Digite o ID do cliente: ")
            list_payments(customer_id)
        elif option.lower() == "quit":
            break
        else:
            print("Opção inválida")

