from OpenSSL import crypto

from .config import Config





conf = {
    'connection':{
        'host': {
            'default':'0.0.0.0',
            'desc': 'host interface to listen on for incoming tls connections'
        },
        'port':{
            'default':8080,
            'desc': 'port to listen on for incoming tls connections'
        },
    },
    'tls':{
        'CN': {
            'default':'localhost',
            'desc': "hostname to be used for certificate CN. If it doesn't match the connection hostname, certificate verification will fail."
        }
    }
}



def prompt_configs():
    print('Fill out configs: (empty for default, ? for info)')
    for key, elem in conf.items():
        if('default' not in elem):
            Config()[key] = {}
            for subkey in elem:
                flag=True
                while(flag):
                    flag=False
                    v = input(f"[{key}][{subkey}] ({conf[key][subkey]['default']}): ")
                    if(v=='?'):
                        flag=True
                        print(conf[key][subkey]['desc'])

                Config()[key][subkey] = v or conf[key][subkey]['default']
        else:
            flag=True
            while(flag):
                flag=False
                v = input(f"[{key}] ({conf[key]['default']}): ")
                if(v=='?'):
                    flag=True
                    print(conf[key]['desc'])
            Config()[key] = v or conf[key]['default']



def shellman_wizard():
    prompt_configs()
    cert, key = cert_gen()
    Config()['tls']['cert'] = cert
    Config()['tls']['key'] = key

    discord()

    Config().write()


def discord():
    Config()['discord_frontend'] = {
        'token': '',
        'admin_mode': True,
        'guild': 702911703301619742,
        'channel': 702911703301619746,
        'category': 'shells',
        'channel_scheme': 'shellman-'
                          '{shell.connection.writer.get_extra_info("peername")[0].replace(".", "-")}-'
                          '{shell.connection.id}'
    }


def cert_gen():
    # create a key pair
    k = crypto.PKey()
    k.generate_key(crypto.TYPE_RSA, 4096)
    # create a self-signed cert
    cert = crypto.X509()
    cert.get_subject().C = 'KP'
    cert.get_subject().ST = 'Pyongyang'
    cert.get_subject().L = 'Shellman'
    cert.get_subject().O = 'Shellman'
    cert.get_subject().OU = 'Shellman'
    cert.get_subject().CN = Config()['tls']['CN']
    cert.get_subject().emailAddress = 'sh@ellm.an'
    cert.set_serial_number(0)
    cert.gmtime_adj_notBefore(0)
    cert.gmtime_adj_notAfter(10 * 365 * 24 * 60 * 60)
    cert.set_issuer(cert.get_subject())
    cert.set_pubkey(k)
    cert.sign(k, 'sha512')
    cert = crypto.dump_certificate(crypto.FILETYPE_PEM, cert).decode('utf-8')
    key = crypto.dump_privatekey(crypto.FILETYPE_PEM, k).decode('utf-8')

    return cert, key
