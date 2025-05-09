#!/usr/bin/env python3
"""
Script para automatizar la descarga de imágenes ISO y generar archivos OVA usando VirtualBox.
Requisitos:
- Python 3.6+
- requests (pip install requests)
- VirtualBox instalado y disponible en el PATH
- VBoxManage accesible desde la línea de comandos
"""

import os
import sys
import time
import subprocess
import argparse
import requests
from urllib.parse import urlparse
from pathlib import Path


def parse_arguments():
    """Analiza los argumentos de línea de comandos."""
    parser = argparse.ArgumentParser(description='Descarga automática de ISO y creación de OVA')
    parser.add_argument('--iso-url', required=True, help='URL de la imagen ISO a descargar')
    parser.add_argument('--vm-name', required=True, help='Nombre de la máquina virtual a crear')
    parser.add_argument('--os-type', default='Ubuntu_64', help='Tipo de sistema operativo (Ubuntu_64, Windows10_64, etc.)')
    parser.add_argument('--os-version', default='', help='Versión del sistema operativo (ya no necesario)')
    parser.add_argument('--memory', type=int, default=2048, help='Memoria RAM en MB')
    parser.add_argument('--cpus', type=int, default=2, help='Número de CPUs')
    parser.add_argument('--disk-size', type=int, default=20000, help='Tamaño del disco en MB')
    parser.add_argument('--output-dir', default='.', help='Directorio para guardar los archivos')
    parser.add_argument('--list-os-types', action='store_true', help='Listar todos los tipos de OS disponibles')
    return parser.parse_args()


def download_iso(url, output_dir):
    """Descarga una imagen ISO desde la URL proporcionada."""
    filename = os.path.basename(urlparse(url).path)
    output_path = os.path.join(output_dir, filename)
    
    # Verificar si el archivo ya existe
    if os.path.exists(output_path):
        print(f"El archivo {filename} ya existe. Omitiendo descarga.")
        return output_path
    
    print(f"Descargando {url} a {output_path}...")
    
    # Descargar con soporte para progreso
    with requests.get(url, stream=True) as r:
        r.raise_for_status()
        total_size = int(r.headers.get('content-length', 0))
        
        os.makedirs(output_dir, exist_ok=True)
        
        with open(output_path, 'wb') as f:
            downloaded = 0
            for chunk in r.iter_content(chunk_size=8192):
                if chunk:
                    f.write(chunk)
                    downloaded += len(chunk)
                    # Mostrar progreso
                    if total_size > 0:
                        percent = int(100 * downloaded / total_size)
                        sys.stdout.write(f"\rProgreso: {percent}% [{downloaded} / {total_size} bytes]")
                        sys.stdout.flush()
            
            if total_size > 0:
                sys.stdout.write("\n")
    
    print(f"Descarga completada: {output_path}")
    return output_path


def run_vboxmanage(cmd):
    """Ejecuta un comando VBoxManage y devuelve su salida."""
    full_cmd = ["VBoxManage"] + cmd
    print(f"Ejecutando: {' '.join(full_cmd)}")
    
    try:
        result = subprocess.run(full_cmd, check=True, text=True, capture_output=True)
        return result.stdout.strip()
    except subprocess.CalledProcessError as e:
        print(f"Error al ejecutar VBoxManage: {e}")
        print(f"Salida: {e.stdout}")
        print(f"Error: {e.stderr}")
        raise


def list_os_types():
    """Lista todos los tipos de sistemas operativos disponibles en VirtualBox."""
    try:
        output = run_vboxmanage(["list", "ostypes"])
        print("Tipos de sistemas operativos disponibles:")
        print(output)
    except subprocess.CalledProcessError:
        print("No se pudo obtener la lista de sistemas operativos.")

def create_virtual_machine(vm_name, os_type, os_version, memory, cpus, disk_size, iso_path, output_dir):
    """Crea una máquina virtual con VirtualBox y la configura."""
    try:
        # Verificar si la máquina virtual ya existe
        try:
            run_vboxmanage(["showvminfo", vm_name])
            print(f"La máquina virtual '{vm_name}' ya existe. Eliminándola...")
            run_vboxmanage(["unregistervm", vm_name, "--delete"])
        except subprocess.CalledProcessError:
            pass  # La VM no existe, lo cual está bien
        
        # Crear la máquina virtual
        print(f"Creando la máquina virtual '{vm_name}'...")
        # Usar directamente el ostype sin concatenar para evitar errores
        ostype = os_version if os_version else os_type
        run_vboxmanage(["createvm", "--name", vm_name, "--ostype", ostype, "--register"])
        
        # Configurar memoria y CPU
        print("Configurando memoria y CPU...")
        run_vboxmanage(["modifyvm", vm_name, "--memory", str(memory), "--cpus", str(cpus)])
        
        # Configurar hardware
        run_vboxmanage(["modifyvm", vm_name, "--acpi", "on", "--ioapic", "on"])
        run_vboxmanage(["modifyvm", vm_name, "--boot1", "dvd", "--boot2", "disk", "--boot3", "none", "--boot4", "none"])
        
        # Configurar red
        run_vboxmanage(["modifyvm", vm_name, "--nic1", "nat"])
        
        # Crear disco duro virtual
        vdi_path = os.path.join(output_dir, f"{vm_name}.vdi")
        print(f"Creando disco duro virtual de {disk_size}MB...")
        run_vboxmanage(["createmedium", "disk", "--filename", vdi_path, "--size", str(disk_size)])
        
        # Añadir controlador SATA
        run_vboxmanage(["storagectl", vm_name, "--name", "SATA Controller", "--add", "sata", "--controller", "IntelAHCI"])
        
        # Adjuntar el disco duro
        run_vboxmanage(["storageattach", vm_name, "--storagectl", "SATA Controller", "--port", "0", "--device", "0", "--type", "hdd", "--medium", vdi_path])
        
        # Añadir controlador IDE
        run_vboxmanage(["storagectl", vm_name, "--name", "IDE Controller", "--add", "ide"])
        
        # Adjuntar la ISO
        run_vboxmanage(["storageattach", vm_name, "--storagectl", "IDE Controller", "--port", "0", "--device", "0", "--type", "dvddrive", "--medium", iso_path])
        
        print(f"Máquina virtual '{vm_name}' creada y configurada correctamente")
        return True
    
    except Exception as e:
        print(f"Error al crear la máquina virtual: {e}")
        return False


def export_to_ova(vm_name, output_dir):
    """Exporta la máquina virtual a un archivo OVA."""
    ova_path = os.path.join(output_dir, f"{vm_name}.ova")
    print(f"Exportando la máquina virtual '{vm_name}' a '{ova_path}'...")
    
    try:
        run_vboxmanage(["export", vm_name, "--output", ova_path])
        print(f"Máquina virtual exportada correctamente a: {ova_path}")
        return ova_path
    except Exception as e:
        print(f"Error al exportar la máquina virtual: {e}")
        return None


def main():
    """Función principal del script."""
    args = parse_arguments()
    
    # Si se solicitó listar los tipos de OS, solo hacemos eso y terminamos
    if args.list_os_types:
        list_os_types()
        return 0
    
    # Verificar que el módulo de kernel esté cargado
    try:
        # Ejecutar un comando simple de VBoxManage para verificar si funciona
        subprocess.run(["VBoxManage", "--version"], check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    except subprocess.CalledProcessError:
        print("\n⚠️  ADVERTENCIA: VirtualBox no está funcionando correctamente.")
        print("Por favor, ejecute el siguiente comando para cargar el módulo del kernel:")
        print("    sudo /sbin/vboxconfig")
        print("Luego intente ejecutar este script nuevamente.\n")
        return 1
    except FileNotFoundError:
        print("\n❌ ERROR: VBoxManage no se encuentra. ¿Está VirtualBox instalado?")
        print("Instale VirtualBox y asegúrese de que VBoxManage esté en su PATH.\n")
        return 1
    
    # Crear directorio de salida si no existe
    os.makedirs(args.output_dir, exist_ok=True)
    
    # Descargar la ISO
    iso_path = download_iso(args.iso_url, args.output_dir)
    
    if not iso_path:
        print("Error: No se pudo descargar la imagen ISO")
        return 1
    
    # Crear máquina virtual
    success = create_virtual_machine(
        args.vm_name,
        args.os_type,
        args.os_version,
        args.memory,
        args.cpus,
        args.disk_size,
        iso_path,
        args.output_dir
    )
    
    if not success:
        print("Error: No se pudo crear la máquina virtual")
        return 1
    
    # Exportar a OVA
    ova_path = export_to_ova(args.vm_name, args.output_dir)
    
    if not ova_path:
        print("Error: No se pudo exportar la máquina virtual a formato OVA")
        return 1
    
    print("\nResumen:")
    print(f"ISO descargada: {iso_path}")
    print(f"Máquina virtual creada: {args.vm_name}")
    print(f"Archivo OVA generado: {ova_path}")
    
    return 0


if __name__ == "__main__":
    sys.exit(main())