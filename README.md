# Fix Parser

Parses raw fix-messages and returns tag-names and known values in a json format example:

```json
{
 "10000": "OBVK67",
 "527": "DBL0F1-7",
 "775": "AAA",
 "AvgPx": "0.000000",
 "BeginString": "FIX.4.2",
 "BodyLength": "230",
 "CheckSum": "252",
 "ClOrdID": "DV_15157",
 "CumQty": "0",
 "Currency": "SEK",
 "ExecID": "DBL0F1-7",
 "ExecTransType": "NEW",
 "ExecType": "REPLACE",
 "LastPx": "0",
 "LastShares": "0",
 "LeavesQty": "30",
 "MsgType": "EXECUTION_REPORT",
 "OrdStatus": "REPLACED",
 "OrdType": "LIMIT",
 "OrderID": "456",
 "OrderQty": "30",
 "OrigClOrdID": "DV_15156",
 "Price": "166.0",
 "SecurityExchange": "ST",
 "SenderCompID": "LLVE_1",
 "Side": "SELL_SHORT",
 "Symbol": "VOLVb.ST",
 "TargetCompID": "FIX2",
 "TimeInForce": "DAY",
 "TransactTime": "20171017-07:16:01.269"
}
```

## Usage

Can read quickfix message logs:

```bash
$ ./fixparser.py --dictionary=fixspecs/FIX50SP2.xml test.log
```

Can read from pipe:

```bash
$ cat test.messages | ./fixparser.py --dictionary=fixspecs/FIX42.xml --delimiter="|" -
```

Can read Raw Messages

```bash
$ ./fixparser.py --dictionary=fixspecs/FIX42.xml --delimiter="|" "8=FIX.4.2|9=155|35=D|49=FIX2|56=LLVE_1|52=20171017-07:15:51.645|34=32|40=2|54=5|55=VOLVb.ST|11=DV_15156|21=3|60=20171017-07:15:51|38=20|44=166.0|59=0|15=SEK|100=ST|207=ST|10=129|"
```
