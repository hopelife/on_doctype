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


## Quote

> quote0
> > quote0-0
> > quote0-1 [link1](url1) quote mark1 $$E=MC^2$$ text
> > > quote0-0-1 **bold** quote mark2
> > > > quote0-0-1-0 *italic* -> quote0-0-2
> > quote0-0-1-0  -> quote0-0-2


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

### Bulleted List

- 리스트 (1)
  - 리스트 (1-1)
  - 리스트 (1-2)
- 리스트 (2)
  - 리스트 (2-1)
  - 리스트 (2-2)

* 빨강
  * 녹색
    * 검정
    * 하양
  * 노랑
    * 파랑

+ 빨강
  + 녹색
    + 파랑

- 빨강
  - 녹색
    - 파랑


* 1단계
  - 2단계
    + 3단계
      + 4단계


### Numbered List

1. 리스트 1
  1-1. 리스트 1-1
    1-1-1. 리스트 1-1-1
2. 리스트 2

### TODO List

[] 할 일1
  [X] 한 일1
  [] 한 일1
    [] 한 일1  

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

image inline ![image1](https://images.unsplash.com/photo-1511300636408-a63a89df3482?ixlib=rb-1.2.1&q=85&fm=jpg&crop=entropy&cs=srgb) test

## Font

this is font *single asterisks* _single underscores_ **double asterisks** ~~cancelline~~  test

