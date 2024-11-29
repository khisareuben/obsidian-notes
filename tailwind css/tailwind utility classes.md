
### Tailwind CSS Utility Classes

#### Colors

- **Text Colors**: `text-black`, `text-white`, `text-gray-100`, ..., `text-gray-900`, `text-red-500`, `text-blue-500`, etc.
    
- **Background Colors**: `bg-black`, `bg-white`, `bg-gray-100`, ..., `bg-gray-900`, `bg-red-500`, `bg-blue-500`, etc.
    
- **Border Colors**: `border-black`, `border-white`, `border-gray-100`, ..., `border-gray-900`, `border-red-500`, `border-blue-500`, etc.
- **Arbitrary Colors**: `text-[#002147]`, `bg-[#002147]`
    
#### Text Decoration

- **Underline**: `underline decoration-4`, `underline decoration-solid`, `underline decoration-double` `dotted dashed wavy`
- **line-through**: `line-through decoration-1` 
- **overline**: `overline`
- **offset**: `underline underline-offset-2` spacing between the text decoration line and the text
- **text transform**: `normal-case`, `uppercase`, `lowercase`, `capitalize` 
#### Typography
     
- **Font Family**: `font-sans`, `font-serif`, `font-mono`
    
- **Font Size**: `text-xs`, `text-sm`, `text-base`, `text-lg`, `text-xl`, `text-2xl`, ..., `text-6xl`
    
- **Font Weight**: `font-thin`, `font-extralight`, `font-light`, `font-normal`, `font-medium`, `font-semibold`, `font-bold`, `font-extrabold`, `font-black`
    
- **Line Height**: `leading-none`, `leading-tight`, `leading-snug`, `leading-normal`, `leading-relaxed`, `leading-loose`
    
- **Letter Spacing**: `tracking-tighter`, `tracking-tight`, `tracking-normal`, `tracking-wide`, `tracking-wider`, `tracking-widest`
    
- **Text Alignment**: `text-left`, `text-center`, `text-right`, `text-justify`
    

#### Layout

- **Display**: `block`, `inline-block`, `inline`, `flex`, `inline-flex`, `grid`, `inline-grid`, `table`, `inline-table`, `table-caption`, `table-cell`, `table-column`, `table-column-group`, `table-footer-group`, `table-header-group`, `table-row-group`, `table-row`, `hidden`
    
- **Position**: `static`, `fixed`, `absolute`, `relative`, `sticky`
    
- **Top/Right/Bottom/Left**: `top-0`, `right-0`, `bottom-0`, `left-0`, `top-1`, `right-1`, `bottom-1`, `left-1`, etc.
    

#### Flexbox and Grid

- **Flex Direction**: `flex-row`, `flex-row-reverse`, `flex-col`, `flex-col-reverse`
    
- **Flex Wrap**: `flex-wrap`, `flex-wrap-reverse`, `flex-nowrap`
    
- **Align Items**: `items-start`, `items-center`, `items-end`, `items-baseline`, `items-stretch`
- - `flex`, `flex flex-col`
- **order**: `order-1` `order-2` ... it will push the div to the order number you specify 
- `flex-none`, `flex-initial`, `flex-auto`, `flex-1`  deals with growing and shrinking

    
- **Justify Content**: `justify-start`, `justify-center`, `justify-end`, `justify-between`, `justify-around`, `justify-evenly`
    
- **Grid Template Columns**: `grid-cols-1`, `grid-cols-2`, `grid-cols-3`, ..., `grid-cols-12 gap-4`
- **span**: `col-span-2` this takes two columns `row-span-2`
    
- **Grid Column Start/End**: `col-start-1`, `col-end-2`, etc.
    
- **Grid Template Rows**: `grid-rows-1`, `grid-rows-2`, `grid-rows-3`, ..., `grid-rows-6`
    

#### Spacing

- **Margin**: `m-0`, `m-1`, `m-2`, `m-4`, `m-8`, `m-auto`, `mx-0`, `mx-1`, ..., `my-8`, `ml-0`, ..., `mr-8` m-[20px]
    
- **Padding**: `p-0`, `p-1`, `p-2`, `p-4`, `p-8`, `px-0`, `px-1`, ..., `py-8`, `pl-0`, ..., `pr-8`  p-[20px]
    
- **Space Between**: `space-x-1`, `space-x-2`, `space-x-4`, `space-y-1`, `space-y-2`, `space-y-4`

#### position

- `static`, `fixed`, `absolute`, `relative`, `sticky` 
- **Display**: `block` `inline` `inline-block` `hidden` 
#### Sizing

- **Width**: `w-0`, `w-1`, `w-2`, `w-4`, `w-8`, `w-auto`, `w-full`, `w-screen` percentage; `w-1/2` `w-1/3` `w-2/5` 
- max-width: `max-w-lg` `max-w-3xl` `max-w-sm`
- arbitrary w-[500px]
    
- **Height**: `h-0`, `h-1`, `h-2`, `h-4`, `h-8`, `h-auto`, `h-full`, `h-screen`
    

#### Borders

- **Border Radius**: `rounded-none`, `rounded-sm`, `rounded`, `rounded-md`, `rounded-lg`, `rounded-full`, `rounded-t`, `rounded-r`, `rounded-b`, `rounded-l`, `rounded-tl`, `rounded-tr`, `rounded-br`, `rounded-bl`
- `border-4 border-red-500` `border-r-4`
    
- **Border Width**: `border-0`, `border-2`, `border-4`, `border-8`
    
- **Border Opacity**: `border-opacity-0`, `border-opacity-25`, `border-opacity-50`, `border-opacity-75`, `border-opacity-100`
    

#### Effects

- **Box Shadow**: `shadow-xs`, `shadow-sm`, `shadow`, `shadow-md`, `shadow-lg`, `shadow-xl`, `shadow-2xl`, `shadow-inner`, `shadow-outline`, `shadow-none` color 
- `shadow-lg shadow-gray-300/40` the 40 is opacity
    
- **Opacity**: `opacity-0`, `opacity-25`, `opacity-50`, `opacity-75`, `opacity-100`

- **gradient**: `bg-gradient-to-r from-pink-100 to-red-500`
`bg-gradient-to-r from-pink-100 via-blue-500 to-red-500`

#### Background

- **Background images**: `bg-cover bg-no-repeat bg-center`
- syle="background-image: url(image-path)   `this comes after the class, inline styling` 
- **Background Size**: `bg-auto`, `bg-cover`, `bg-contain`
    
- **Background Position**: `bg-bottom`, `bg-center`, `bg-left`, `bg-left-bottom`, `bg-left-top`, `bg-right`, `bg-right-bottom`, `bg-right-top`, `bg-top`
    

#### images and filters
- **contrast**: `contrast-50` `contrast-100` `contrast-125` ... deals with color
- **brightness**: `brightness-50` .... deals with light
- **grayscale**: `grayscale-0`, `grayscale` `invert` `sepia` deals with filters
- **hue**: `hue-rotate-0` `hue-rotate-15` rotates the hue or an image
- **saturate**: `saturate-100`
- **blur**: `blur-none`, `blur-sm`, `blur-lg`, `blur-2xl`


#### media queries

- `sm`, `md` `lg` `xl` `2xl`
- `sm:w-32 lg:w-48`


#### Transition

- `transition duration-300 ease-in-out delay-150 `

#### Transformation

- `hover:-translate-y-1 hover:scale-110 hover:bg-teal-500`
this will make it bigger once you hover 


#### Animation

- `animate-spin`, `animate-ping`, `animate-pulse`, `animate-bounce`
- `motion-safe:animate-spin` reduces motion

	
 #### Pseudo-Classes

- **Hover, Focus, Active**: `hover:bg-blue-500`, `focus:bg-blue-500`, `active:bg-blue-500`
    
- **Responsive**: `sm:bg-blue-500`, `md:bg-blue-500`, `lg:bg-blue-500`, `xl:bg-blue-500`