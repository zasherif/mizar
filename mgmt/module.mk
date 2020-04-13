
module := mgmt
GRPC_FLAGS := -I mgmt/proto --python_out=mgmt/proto --grpc_python_out=mgmt/proto

.PHONY: proto
proto:
	python3 -m grpc_tools.protoc $(GRPC_FLAGS) mgmt/proto/*.proto

clean::
	rm -rf mgmt/proto/__pycache__
	find mgmt/proto/ -name '*.py' -not -name '__init__.py' -delete
