# Module zoo_wes_runner.base

Bases classes for Zoo runners.

These are derived here from the zoo-calrissian-runner because no generic abstract classes exist.

## Variables

```python3
logger
```

## Classes

### BaseZooRunner

```python3
class BaseZooRunner(
    cwl,
    conf,
    inputs,
    outputs,
    execution_handler: Optional[zoo_calrissian_runner.handlers.ExecutionHandler] = None
)
```

Mangle the ZooCalrissianRunner to be a base class to inherit from.

#### Ancestors (in MRO)

* zoo_calrissian_runner.ZooCalrissianRunner

#### Descendants

* zoo_wes_runner.wes_runner.ZooWESRunner

#### Static methods

    
#### shorten_namespace

```python3
def shorten_namespace(
    value: str
) -> str
```

shortens the namespace to 63 characters

#### Methods

    
#### assert_parameters

```python3
def assert_parameters(
    self
)
```

checks all mandatory processing parameters were provided

    
#### execute

```python3
def execute(
    self
)
```

This function should be implmented to provide job exection logic.

    
#### get_max_cores

```python3
def get_max_cores(
    self
) -> int
```

returns the maximum number of cores that pods can use

    
#### get_max_ram

```python3
def get_max_ram(
    self
) -> str
```

returns the maximum RAM that pods can use

    
#### get_namespace_name

```python3
def get_namespace_name(
    self
)
```

creates or returns the namespace

    
#### get_processing_parameters

```python3
def get_processing_parameters(
    self
)
```

Gets the processing parameters from the zoo inputs

    
#### get_volume_size

```python3
def get_volume_size(
    self
) -> str
```

returns volume size that the pods share

    
#### get_workflow_id

```python3
def get_workflow_id(
    self
)
```

returns the workflow id (CWL entry point)

    
#### get_workflow_inputs

```python3
def get_workflow_inputs(
    self,
    mandatory=False
)
```

Returns the CWL workflow inputs

    
#### prepare

```python3
def prepare(
    self
)
```

Generic pre-execution which applies to all handlers.

    
#### update_status

```python3
def update_status(
    self,
    progress: int,
    message: str = None
) -> None
```

updates the execution progress (%) and provides an optional message

    
#### wrap

```python3
def wrap(
    self
)
```