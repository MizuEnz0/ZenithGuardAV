rule RANSOMWARE_GENERIC_CRYPTO_APIS {
    meta:
        author = "ZenithGuard"
        description = "Detecta binários que importam funções comuns de criptografia Windows/Linux"
        score = 80
        
    strings:
        // Funções de Criptografia Comuns (Windows)
        $a1 = "CryptGenKey" ascii wide
        $a2 = "CryptEncrypt" ascii wide
        $a3 = "CryptDestroyKey" ascii wide
        $a4 = "CryptAcquireContext" ascii wide
        
        // Funções de I/O de Arquivo (para varrer discos)
        $b1 = "GetLogicalDrives" ascii wide
        $b2 = "FindFirstFile" ascii wide
        
        // Criação de Thread/Processo (para persistência ou execução)
        $c1 = "CreateProcessA" ascii wide
        $c2 = "CreateThread" ascii wide
        
    condition:
        // Exige que seja um executável (MZ) E pelo menos três APIs de criptografia
        // ou três APIs de varredura/processo
        uint16(0) == 0x5a4d and (3 of ($a*) or 3 of ($b*, $c*))
}

rule RANSOMWARE_FILE_RENAME_PATTERN {
    meta:
        author = "ZenithGuard"
        description = "Detecta padrão de criação de arquivos com novas extensões"
        score = 70
        
    strings:
        // Extensões de Ransomware Comuns
        $e1 = ".locky" ascii wide
        $e2 = ".vault" ascii wide
        $e3 = ".crypt" ascii wide
        $e4 = ".vvv" ascii wide
        $e5 = "HOW_TO_DECRYPT" ascii wide // Nota de resgate comum
        $e6 = "READ_ME" ascii wide // Nota de resgate comum
        
    condition:
        // Deve ser um executável E corresponder a pelo menos 3 dessas strings
        uint16(0) == 0x5a4d and 3 of ($e*)
}

rule WANNACRY_GENERIC_STRINGS {
    meta:
        author = "ZenithGuard"
        description = "Identifica strings conhecidas da família WannaCry/WanaCrypt0r"
        family = "WannaCry"
        score = 95
        
    strings:
        // Strings presentes no binário do WannaCry
        $s1 = "WNcry@2ol7" ascii wide
        $s2 = "tasksche.exe" ascii fullword
        $s3 = "PleasePayMoreAttention.xml" ascii wide
        $s4 = "Icacls . /grant Everyone:F /T /C /Q" ascii wide // Comando para alterar permissões
        $s5 = "0x00010000" ascii // Um valor de constante usado no código
        
    condition:
        // Exige o cabeçalho PE (uint16(0) == 0x5a4d) E pelo menos 3 dessas strings
        uint16(0) == 0x5a4d and 3 of ($s*)
}

rule RANSOMWARE_KILLSWITCH_FAIL {
    meta:
        author = "ZenithGuard"
        description = "Busca pelo domínio de Killswitch do WannaCry (falha na conexão indica ransomware ativo)"
        family = "WannaCry"
        score = 90
        
    strings:
        // O famoso domínio 'kill switch' (que o ransomware tenta acessar)
        $d1 = "iuqerfsodp9ifjaposdfjhgosurijfaewrwergwea.com" ascii wide
        
    condition:
        // A presença do domínio indica o código do WannaCry
        uint16(0) == 0x5a4d and $d1
}