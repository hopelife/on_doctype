# Block Test

## Heading

## Heading_2: Line endings are **important** not only in Markdown...

### Heading_3: Line endings are **important** not only in Markdown...

#### Heading_4: Line endings are **important** not only in Markdown...


## Paragraph

### Paragraph without indent

Paragraph1
Line.\
Another line because the previous ends with a "\\".

### Paragraph with indent

This is a normal paragraph:
    This is a indented block1.
    This is a indented block2.
end code block.



## Code blocks

Java code:

```java
public class Main {
    public static void main(String[] args) {
        System.out.println("Hello World!");
    }
}
```

Log file:

    2020-07-05 10:20:55 ...
    2020-07-05 10:20:56 ...
        ...
    2020-07-05 10:21:03 ...


# Others

## List


## Table

### With Header

| Column_A | Column_B | Column_C |
| ---------|----------|---------| 
|  A1 | *B1* | C1 |
|  A2 | B2 | C2 |
|  A3 | B3 | C3 |


### Without Header
| Column_A | Column_B | Column_C |
|  A1 | B1 | C1 |
|  A2 | _B2_ | C2 |
|  A3 | B3 | C3 |

# Span Test

## Link

this is link [link1](https://a.b.com) test

* 외부링크: <http://example.com/>
* 이메일링크: <address@example.com>

## Image

image inline 
![image1](https://images.unsplash.com/photo-1511300636408-a63a89df3482?ixlib=rb-1.2.1&q=85&fm=jpg&crop=entropy&cs=srgb) test

## Font

this is font *single asterisks* _single underscores_ **double asterisks** ~~cancelline~~  test

