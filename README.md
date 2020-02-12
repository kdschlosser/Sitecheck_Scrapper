# MobileActivity

Mobile application to assist field techs with setting up Job activities in the Vortex app on Quickbase.

## Devolpment cycle:

#### Phase 1: Build scanner
 1. Using inidivually created profiles for each job, query user for remaining information to create new activity with.
 2. Create a record on quickbase with user data
 3. Packaged Android 10 APK

#### Phase 2:
 1. Add option to update previously created records
 2. Add verfication-of-record-creation notice from quickbase
 3. Add local fallback wait-for-wifi options and failure call backs.
 4. Packaged iOS 13.3 IPA

#### Phase 3:
 1. Test Android 9, iOS 12, and below OSs
 2. Add user to log in and use stored profile data.
 3. Use the quickbase API to query Customer/Jobs/SO#s and autofill these fields for input
 4. Implement security options to protect sensitive data

#### Phase 4: Experimental goals
 1. Timesheet modual
 2. Teams intergration
 3. Retrieve/edit job-assigned asset entries



## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes. See deployment for notes on how to deploy the project on a live system.

### Prerequisites

What things you need to install the software and how to install them.

```
Required:
    Suggested:

```

### Installing

A step by step series of examples that tell you how to get a development env running

Say what the step will be

```
Give the example
```

And repeat

```
until finished
```

End with an example of getting some data out of the system or using it for a little demo

## Running the tests

Explain how to run the automated tests for this system

### Break down into end to end tests

Explain what these tests test and why

```
Give an example
```

## Comments on style
Functions are styled in snake_case.  
```
login()
scan_plan_view()  
watchdog_processor()  
```
Classes are styled using CapWords
```
Project_Run
Amp_website
QV_website
```


### And coding style tests

Explain what these tests test and why

```
Give an example
```
## Deployment

TODO: Add additional notes about how to deploy this on a live system

## Built With

[Python v3.8.1](https://docs.python.org/3.8/)  
[Pyppeteer v0.2.5](https://miyakogi.github.io/pyppeteer/)   


## Contributing

Please read [CONTRIBUTING.md](https://geodev.geo-instruments.com/DanEdens/mobileactivity/blob/master/CONTRIBUTING.md) for details on our code of conduct, and the process for submitting pull requests to us.

## Versioning

Project repository can be found at [MobileActivity](https://geodev.geo-instruments.com/DanEdens/pyppet_sitecheck_scrapper).

## Author

* **Dan Edens** - [Dan.Edens](https://github.com/DanEdens)


## License

TODO:

## Acknowledgments

* etc
