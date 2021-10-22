# Message Templates

**When it comes to sending LinkedIn connection request messages, `inb` has got your back.**

By using the right kind of template, you can be sure that many new opportunities will be flooding your inbox in no time at all.

**Remember, use template that best suit your needs.**

## Template variables

Before looking at the template I want you to look at the variables that **inb** uses for message template.

- `{{name}}`: Person full name you are sending request to.
- `{{first_name}}`: Person first name you are sending request to.
- `{{last_name}}`: Person last name you are sending request to.
- `{{my_name}}`: Your full name.
- `{{my_first_name}}`: Your first name.
- `{{my_last_name}}`: Your last name.
- `{{keyword}}`: Keyword you typed in over command line.
- `{{location}}`: Location you specified over command line. In case you specified multiple locations then the location on Person
  profile will be used.
- `{{industry}}`: Industry you specified over command line. In case you specified multiple industries then the industry on Person
  profile will be used.
- `{{title}}`: Title you typed in over command line.
- `{{school}}`: School you typed in over command line.
- `{{current_company}}`: Current company you typed in over command line.
- `{{profile_language}}`: Profile language you typed in over command line.
- `{{my_position}}`: Your position at your company.
- `{{my_company_name}}`: Your company name.
- `{{position}}`: Position you are looking an employee for.
- `{{year}}`: Current year.

This document has the following content available:

- [Personalized Templates](#personalized-templates)
- [Templates with Subtle Pitch](#templates-with-subtle-pitch)
- [Webinar Invitation](#webinar-invitation)
- [Common Connection Request Messages](#common-connection-request-messages)
- [How you can add your own?](#how-you-can-add-your-own)

## Personalized Templates

- Assumes that the person owns some business.

  ```text
  Hi {{name}},

  I'm looking to expand my network with fellow business owners and professionals. I would love to learn about what you do and see
  if there's any way we can support each other.

  Cheers!
  ```

  Example:

  ```shell
  python3 inb/inb.py search --email "ayush854032@gmail.com" --password "F:(:);GVlk\`" --location "Australia" --title "Business Owner" --keyword "Business Owner" message --template-business
  ```

- Assumes that the person belong to a sales job.

  ```text
  Hi {{name}},

  I'm looking to connect with like-minded professionals specifically who are on the revenue generating side of things.

  Let's connect!
  ```

  Example:

  ```shell
  python3 inb/inb.py search --email "ayush854032@gmail.com" --password "F:(:);GVlk\`" --location "Australia" --title "Sales" --keyword "Sales" message --template-sales
  ```

- Assumes that the person works in real estate.

  ```text
  Hey {{name}},

  Came across your profile and saw your work in real estate. I'm reaching out to connect with other like-minded people. Would be
  happy to make your acquaintance.

  Have a good day!
  ```

  Example:

  ```shell
  python3 inb/inb.py search --email "ayush854032@gmail.com" --password "F:(:);GVlk\`" --location "Australia" --title "Real estate" --keyword "Real estate" message --template-real-estate
  ```

- Assumes that you and the person both are in the creative industry.

  ```text
  Hi {{name}},

  LinkedIn showed me your profile multiple times now, so I checked what you do. I really like your work and as we are both in the
  creative industy - I thought I'll reach out. It's always great to be connected with like-minded individuals, isn't it?

  {{my_name}}
  ```

  Example:

  ```shell
  python3 inb/inb.py search --email "ayush854032@gmail.com" --password "F:(:);GVlk\`" --location "Australia" --title "Artist" --keyword "Artist" message --template-creative-industry
  ```

- Assumes that the person and you both work in the HR field.

  ```text
  Hey {{name}},

  I hope your week is off to a great start, I noticed we both work in the HR/Employee Experience field together.

  I would love to connect with you.
  ```

  Example:

  ```shell
  python3 inb/inb.py search --email "ayush854032@gmail.com" --password "F:(:);GVlk\`" --location "Australia" --title "Artist" --keyword "Artist" message --template-hr
  ```

- Includes industry.

  ```text
  Hi {{name}},

  I hope you're doing great! I'm on a personal mission to grow my connections on LinkedIn, especially in the field of {{industry}}.
  So even though we're practically strangers, I'd love to connect with you.

  Have a great day!
  ```

  Example:

  ```shell
  python3 inb/inb.py search --email "ayush854032@gmail.com" --password "F:(:);GVlk\`" --location "Australia" --title "Artist" --keyword "Artist" message --template-include-industry
  ```

## Templates with Subtle Pitch

- Ben Franklin effect

  ```text
  Hi {{name}},

  The Ben Franklin effect - when we do a person a favor, we tend to like them more as a result. Anything I can do for you?

  Best, {{my_name}}
  ```

  Example:

  ```shell
  python3 inb/inb.py search --email "ayush854032@gmail.com" --password "F:(:);GVlk\`" --location "Australia" --title "Artist" --keyword "Artist" message --template-ben-franklin
  ```

## Webinar Invitation

- Ask for connecting virtually

  ```text
  Hi {{name}},

  I hope you're doing well. I'm {{my_name}}, {{my_position}} of {{my_company_name}}. We're looking for {{position}} and it would be
  great to connect over a 'virtual' coffee/chat and see what we can do together?
  ```

  Example:

  ```shell
  python3 inb/inb.py search --email "ayush854032@gmail.com" --password "F:(:);GVlk\`" --location "Australia" --title "Artist" --keyword "Artist" message --template-virtual-coffee
  ```

## Common Connection Request Messages

**inb** will choose any of the following template by itself if you use the flag `--template-common-connection-request`.

```text
Hey {{name}},

I notice we share a mutual connection or two & would love to add you to my network of professionals.

If you're open to that let's connect!
```

```text
Hi {{name}},

I see we have some mutual connections. I always like networking with new people, and thought this would be an easy way for us to
introduce ourselves.
```

```text
Hi {{name}},

Life is both long and short. We have quite a few mutual connections. I would like to invite you to join my network on LinkedIn
platform. Hopefully, our paths will cross professionally down the line. Until then, wishing you and yours an incredible {{year}}.

{{my_name}}
```

```text
Hi {{name}},

I was looking at your profile and noticed we had a few shared connections. I thought it would be nice to reach out to connect with
you and share out networks.

Thank you and hope all is well!
```

```text
Hey {{first_name}},

I saw you're based in {{location}} and work on {{keyword}}, I'd love to connect.

Thanks, {{my_name}}
```

Example:

```shell
python3 inb/inb.py search --email "ayush854032@gmail.com" --password "F:(:);GVlk\`" --location "Australia" --title "Artist" --keyword "Artist" message --template-common-connection-request
```

## How you can add your own?

You can also add your own message template when using **inb**. You have to add your message in a file and later you have to specify
that file over command line.

For example,

**message.txt**

```text
Hi {{name}},

Life is both long and short. We have quite a few mutual connections. I would like to invite you to join my network on LinkedIn
platform. Hopefully, our paths will cross professionally down the line. Until then, wishing you and yours an incredible {{year}}.

{{my_name}}
```

_Note: The file name can be anything._

And later you can specify its path as show below:

```shell
python3 inb/inb.py search --email "ayush854032@gmail.com" --password "F:(:);GVlk\`" --location "Australia" --title "Director"  --keyword "People Management" message "message.txt"
```

You can also add your messages over the command line without making an extra file, for example:

```shell
python3 inb/inb.py search --email "ayush854032@gmail.com" --password "F:(:);GVlk\`" --location "Australia" --title "Director"  --keyword "People Management" message "Hi {{name}}! Would you like to connect?"
```

**Note: You must avoid writing multi-line text messages directly over command line what you should do instead is make a separate file for that.**
