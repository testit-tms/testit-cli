[2.7.0] 17.09.2025

* add `xctest` framework to `autotests_filter` command

Run can be made with this:

```
$ export TMS_TOKEN=<YOUR_TOKEN>
$ testit autotests_filter 
  --url https://tms.testit.software \
  --configuration-id 5236eb3f-7c05-46f9-a609-dc0278896464 \
  --testrun-id 6d4ac4b7-dd67-4805-b879-18da0b89d4a8 \
  --framework xctest \
  --output tmp/filter.txt
  
$ xcodebuild test -scheme tests -only-testing:"$(cat tmp/filter.txt)" 
```

where tests - scheme name