l = [r"C:\Users\amade\Documents\dawd\lofi1\lofi\Mixdown\output\ohio0_00024v2_s",
r"C:\Users\amade\Documents\dawd\lofi1\lofi\Mixdown\output\tok0_00024v2_s",
r"C:\Users\amade\Documents\dawd\lofi1\lofi\Mixdown\output\SA0_00024v2_s",
r"C:\Users\amade\Documents\dawd\lofi1\lofi\Mixdown\output\osa1_00024v2_s",
r"C:\Users\amade\Documents\dawd\lofi1\lofi\Mixdown\output\lond1_00024v2_s"]

for p in l:
    with open (p +  "\\lenght.txt", "r")as fff:
        data = fff.read()
        print(data)