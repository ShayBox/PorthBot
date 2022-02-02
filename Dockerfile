FROM alpine:3.15

# Update package index, upgrade packages, and install dependencies
RUN apk update
RUN apk upgrade
RUN apk add curl git

# Download, unpack, and install fasm
WORKDIR /var/run
RUN curl http://flatassembler.net/fasm-1.73.29.tgz | tar xz
RUN cp fasm/fasm.x64 /usr/bin/fasm
RUN chmod +x /usr/bin/fasm

# Clone and bootstrap porth
RUN git clone https://gitlab.com/tsoding/porth.git
WORKDIR /var/run/porth
RUN ../fasm/fasm -m 524288 ./bootstrap/porth-linux-x86_64.fasm
RUN chmod +x ./bootstrap/porth-linux-x86_64
RUN ./bootstrap/porth-linux-x86_64 com ./porth.porth
RUN ./porth com ./porth.porth

# Create the run script and set entrypoint
RUN echo -e '#!/bin/sh\nprintf %s "$1" > program.porth\n./porth com -r program.porth' > run.sh
RUN chmod +x run.sh
ENTRYPOINT ["./run.sh"]