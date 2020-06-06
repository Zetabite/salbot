import discord
from discord.ext import commands
import time
import math
import gspread

class Random(object):
    """
    An implementation of the Java SE 6 random number generator.
    Java's RNG is based on a classic Knuth-style linear congruential formula,
    as described in
    http://download.oracle.com/javase/6/docs/api/java/util/Random.html. This
    makes it quite trivial to reimplement and port to other platforms.
    This class should be bit-for-bit compatible with any Java RNG.
    This class is not thread-safe. For deterministic behavior, lock or
    synchronize all accesses to this class per-instance.
    """

    def __init__(self, seed = None):
        """
        Create a new random number generator.
        """

        if seed is None:
            seed = int(time.time() * 1000)
        self.seed = seed

        self.nextNextGaussian = None

    def setSeed(self, seed):
        """
        Explicit setter for seed, for compatibility with Java.
        """

        self.seed = seed

    @property
    def seed(self):
        return self._seed

    @seed.setter
    def seed(self, seed):
        self._seed = (seed ^ 0x5deece66d) & ((1 << 48) - 1)

    def next(self, bits):
        """
        Generate the next random number.
        As in Java, the general rule is that this method returns an int that
        is `bits` bits long, where each bit is nearly equally likely to be 0
        or 1.
        """

        if bits < 1:
            bits = 1
        elif bits > 32:
            bits = 32

        self._seed = (self._seed * 0x5deece66d + 0xb) & ((1 << 48) - 1)
        retval = self._seed >> (48 - bits)

        # Python and Java don't really agree on how ints work. This converts
        # the unsigned generated int into a signed int if necessary.
        if retval & (1 << 31):
            retval -= (1 << 32)

        return retval

    def nextBytes(self, l):
        """
        Replace every item in `l` with a random byte.
        """

        for i in range(0, len(l)):
            if not i % 4:
                n = self.nextInt()
            b = n & 0xff
            # Flip signs. Ugh.
            if b & 0x80:
                b -= 0x100
            l[i] = b
            n >>= 8

    def nextInt(self, n = None):
        """
        Return a random int in [0, `n`).
        If `n` is not supplied, a random 32-bit integer will be returned.
        """

        if n is None:
            return self.next(32)

        if n <= 0:
            raise ValueError("Argument must be positive!")

        # This tricky chunk of code comes straight from the Java spec. In
        # essence, the algorithm tends to have much better entropy in the
        # higher bits of the seed, so this little bundle of joy is used to try
        # to reject values which would be obviously biased. We do have an easy
        # out for power-of-two n, in which case we can call next directly.

        # Is this a power of two?
        if not (n & (n - 1)):
            return (n * self.next(31)) >> 31

        bits = self.next(31)
        val = bits % n
        while (bits - val + n - 1) < 0:
            bits = self.next(31)
            val = bits % n

        return val

    def nextLong(self):
        """
        Return a random long.
        Java longs are 64 bits wide, but the generator is only 48 bits wide,
        so we generate two 32-bit numbers and glue them together.
        """

        return (self.next(32) << 32) + self.next(32)

    def nextBoolean(self):
        """
        Return a random bool.
        """

        return bool(self.next(1))

    def nextFloat(self):
        """
        Return a random float in (0, 1).
        Python floats always carry double precision, so this function's return
        values may appear less-than-random, but they are random in single
        precision space.
        """

        return self.next(24) / float(1 << 24)

    def nextDouble(self):
        """
        Return a random float in (0, 1).
        """

        return ((self.next(26) << 27) + self.next(27)) / float(1 << 53)

    def nextGaussian(self):
        """
        Return a normally-distributed double with mean 0 and standard
        deviation 1.
        This method may not be strict enough to perfectly match the produced
        values of Java's Random.nextGaussian().
        """

        if self.nextNextGaussian is None:
            s = 0
            while s == 0 or s >= 1:
                v1 = 2 * self.nextDouble() - 1
                v2 = 2 * self.nextDouble() - 1
                s = v1 * v1 + v2 * v2
            multiplier = math.sqrt(-2 * math.log(s) / s)
            self.nextNextGaussian = v2 * multiplier
            return v1 * multiplier
        else:
            retval = self.nextNextGaussian
            self.nextNextGaussian = None
            return retval

class CactusSim:
    def __init__(self, count, floorLevel):
        self.heightMap = [floorLevel for i in range(32**2)]

        self.count = count
        self.floorLevel = floorLevel

        self.currentHighestPos = 0

    def populate(self, seed):
        random = Random(seed ^ 0x5DEECE66D)

        for i in range(self.count):
            initialPosX = random.nextInt(16) + 8
            initialPosZ = random.nextInt(16) + 8
            terrainHeight = (self.heightMap[initialPosX + initialPosZ * 32] + 1) * 2

            if terrainHeight > 0:
                initialPosY = random.nextInt(terrainHeight)
                self.generateCactus(random, initialPosX, initialPosY, initialPosZ)

        return self.heightMap[self.currentHighestPos] - self.floorLevel

    def generateCactus(self, random, initialPosX, initialPosY, initialPosZ):
        for i in range(10):
            posX = initialPosX + random.nextInt(8) - random.nextInt(8)
            posY = initialPosY + random.nextInt(4) - random.nextInt(4)
            posZ = initialPosZ + random.nextInt(8) - random.nextInt(8)

            if not self.isAir(posX, posY, posZ):
                continue

            offset = 1 + random.nextInt(random.nextInt(3) + 1)
            posMap = posX + posZ * 32

            for j in range(offset):
                if self.isAir(posX, posY + j - 1, posZ):
                    continue
                if not self.isAir(posX + 1, posY + j, posZ):
                    continue
                if not self.isAir(posX - 1, posY + j, posZ):
                    continue
                if not self.isAir(posX, posY + j, posZ + 1):
                    continue
                if not self.isAir(posX, posY + j, posZ - 1):
                    continue

                self.heightMap[posMap] += 1

                if self.heightMap[self.currentHighestPos] < self.heightMap[posMap]:
                    self.currentHighestPos = posMap

    def isAir(self, x, y, z):
        height = self.heightMap[x + z * 32]
        return y > height or y < 0

def generate(seed, floorlevel=63):
    desert = 10
    test = CactusSim(desert, floorlevel)
    cactusheight = test.populate(seed)
    return cactusheight

class CactusHeight(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="cactusheight", aliases=["ch"])
    @commands.has_any_role("Administrator", "Moderator", "Private Chat Access")
    async def cactusheight(self, ctx, stacccyboi):
        kekw = generate(int(stacccyboi))
        await ctx.channel.send(":cactus:That boi stacked " + str(kekw) + " blocks tall!:cactus:")
        row = int (stacccyboi) // 100000000000 + 2
        if(kekw>=10):
            await ctx.channel.send("Put in box " + str(row)+" on the spreadsheet!")
        gc = gspread.service_account(filename='googlekeykaktoos.json')
        sh = gc.open_by_key('1PSz9y2l9Oo4-uoqrf7wB4Gtd_Z8CRAJ34SCrU9aj59E')
        val = worksheet.cell(row, 2).value
        if val is not None and val is not '':
            worksheet.update(row, 2, stacccyboi)
        else:
            worksheet.update(row, 2, (str(val) + ", " + str(stacccyboi)))
        
    @commands.command(name="markdone", aliases=["md"])
    @commands.has_any_role("Administrator", "Moderator", "Private Chat Access")
    async def markdone(self, ctx, markthatshit):
        gc = gspread.service_account(filename='googlekeykaktoos.json')
        sh = gc.open_by_key('1PSz9y2l9Oo4-uoqrf7wB4Gtd_Z8CRAJ34SCrU9aj59E')
        markthatshit = int(int(markthatshit)// 100000000000 + 2)
        fucc = "A{0}:B1".format(markthatshit)
        worksheet.format(str(fucc), {  
            "backgroundColor": {
                "red": 0.0,
                "green": 1.0,
                "blue": 0.0
            }
        })

def setup(bot):
    bot.add_cog(CactusHeight(bot))
