package main

import (
	"fmt"
	globaljsonpb "github.com/gogo/protobuf/jsonpb"
	"github.com/gogo/protobuf/proto"
)

type pm struct {
	Field int `protobuf:"varint,1,opt,name=field,json=field,proto3" json:"field,omitempty"`
}

func (*pm) Reset() {}
func (*pm) String() string { return "" }
func (*pm) ProtoMessage() {}

func Unmarshal(in []byte, v interface{}) (error) {
	mess, ok := v.(proto.Message)
	if !ok {
		return fmt.Errorf("unsupported type %T to unmarshal into", v)
	}

	return globaljsonpb.UnmarshalString(string(in), mess)
}

func main() {
	s := pm{}
	err := Unmarshal([]byte(`{"field":123}`), &s)
	fmt.Printf("err=%v, s=%#v\n", err, s)
}
