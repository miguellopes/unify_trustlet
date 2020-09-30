import sys, os, struct
from elftools.elf.elffile import ELFFile

def main():

    #Reading the arguments
    if len(sys.argv) != 4:
        print("USAGE: <TRUSTLET_DIR> <TRUSTLET_NAME> <OUTPUT_FILE_PATH>")
        return

    trustlet_dir = sys.argv[1]
    trustlet_name = sys.argv[2]
    output_file_path = sys.argv[3]

    #Reading the ELF header from the ".mdt" file
    mdt = open(os.path.join(trustlet_dir, "%s.mdt" % trustlet_name), "rb")
    elf = ELFFile(mdt)
    ##Reading each of the program headers and copying the relevant chunk
    output_file = open(output_file_path, 'wb')
    i = 0
    #Reading each of the program headers and copying the relevant chunk
    for phnum in elf.iter_segments():
        print(f"[+] Reading PHDR {i}")
        print(f"[+] Size: 0x{phnum['p_filesz']:08X}, Offset: 0x{phnum['p_offset']:08X}")
        if phnum['p_filesz'] == 0:
            print("[+] Empty block, skipping")
            i += 1
            continue #There's no backing block

        #Copying out the data in the block
        block = open(os.path.join(trustlet_dir, f"{trustlet_name}.b{i:02d}"), 'rb').read()
        output_file.seek(phnum['p_offset'], 0)
        output_file.write(block)
        i += 1

    mdt.close()
    output_file.close()

if __name__ == "__main__":
    main()
