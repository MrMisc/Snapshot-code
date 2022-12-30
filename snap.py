
@client.command()
async def cam(ctx, website, userinput=5):
    url = website
    path = 'C:/Users/Irshad/Pictures/Saved Pictures/cam.png'
    options = webdriver.ChromeOptions()
    options.headless = True
    driver = webdriver.Chrome('D:/chromedriver.exe',options=options)
    driver.get(url)
    height = driver.execute_script("return document.body.scrollHeight")
    driver.set_window_size(1000, height - 100)
    driver.execute_script(f"window.scrollTo(0, {height/2})")
    driver.execute_script("window.scrollTo(0, 0)")
    driver.set_window_size(1000, height)
    numberofpicstomake = min(int(userinput),height//1000)
    time.sleep(5) # new images need time to load
    S = lambda X: driver.execute_script('return document.body.parentNode.scroll'+X)
    driver.set_window_size(S('Width'),S('Height')) # May need manual adjustment
    tag = 'body'
    loopcount = 0
    while loopcount<1000:
        try:
            if driver.find_element(By.TAG_NAME, tag).screenshot(path): break
        except Exception:
            print("Looping Till Height")
            loopcount+=1
            tag+=' div'
    driver.quit()
    def long_slice(image_path, out_name, outdir, slice_size):
        """slice an image into parts slice_size tall"""
        img = Image.open(image_path)
        width, height = img.size
        upper = 0
        left = 0
        slices = int(math.ceil(height/slice_size))

        count = 1
        listofsplits = []
        for slice in range(slices):
            #if we are at the end, set the lower bound to be the bottom of the image
            if count == slices:
                lower = height
            else:
                lower = int(count * slice_size)
            #set the bounding box! The important bit
            bbox = (left, upper, width, lower)
            working_slice = img.crop(bbox)
            upper += slice_size
            #save the slice
            newpath = f"{outdir}"+ "part" + f"{out_name}" + "_" + str(count)+".png"
            working_slice.save(os.path.join(newpath))
            listofsplits.append(newpath)
            count +=1
        return listofsplits
    guild = ctx.message.guild
    stringthing = f"tea_image_output"
    await guild.categories[4].create_text_channel(stringthing)
    existing_channel = discord.utils.get(ctx.guild.channels, name=stringthing)
    iden = existing_channel.id
    schannel = client.get_channel(iden)
    await schannel.send(ctx.author.mention)
    for newpath in long_slice(path, "2_split", os.getcwd(), height//numberofpicstomake):
        await schannel.send(file=discord.File(newpath))
        os.remove(newpath)
    os.remove(path)
    time.sleep(60)
    await existing_channel.delete()
