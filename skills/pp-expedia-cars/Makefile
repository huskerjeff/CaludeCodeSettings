.PHONY: build test lint install clean

build:
	go build -o bin/expedia-cars-pp-cli ./cmd/expedia-cars-pp-cli

test:
	go test ./...

lint:
	golangci-lint run

install:
	go install ./cmd/expedia-cars-pp-cli

clean:
	rm -rf bin/

build-mcp:
	go build -o bin/expedia-cars-pp-mcp ./cmd/expedia-cars-pp-mcp

install-mcp:
	go install ./cmd/expedia-cars-pp-mcp

build-all: build build-mcp
